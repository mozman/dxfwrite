#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: convert excel to dxf files
# Created: 19.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

# default pen assignment:
# 1 : 1.40mm - red
# 2 : 0.35mm - yellow
# 3 : 0.70mm - green
# 4 : 0.50mm - cyan
# 5 : 0.13mm - blue
# 6 : 1.00mm - magenta
# 7 : 0.25mm - white/black
# 8, 9 : 2.00mm
# >=10 : 1.40mm

import sys
import os
import logging
import locale
import glob
from datetime import datetime
from optparse import OptionParser

import xlrd
from dxfwrite import DXFEngine as dxf
import dxfwrite.const as const
from dxfwrite.std import color_index

locale.setlocale(locale.LC_ALL, "")


HEIGHT_FACTOR = 0.001763671
WIDTH_FACTOR = 0.000764724
FONT_FACTOR = HEIGHT_FACTOR * 0.7
BORDER_COLOR = [5, 7, 4, 3] # none, thin, middle >=2.5pt, thick >= 4.0pt
FPOINT = '.'
COLON = ','
MAX_FLOAT_PREC = 6

DEFAULT_COLUMN_WIDTH = 2.5
DEFAULT_ROW_HEIGHT = 1.0

def grouped_number(number, float_prec, thousend_point=False):
    fmt_str = "%%.%df" % min(float_prec, MAX_FLOAT_PREC)
    return locale.format(fmt_str, number, thousend_point)

class XFRecord(object):
    """Facade for xf_record."""
    def __init__(self, book, xf_index):
        self.book = book
        self.xf_index = xf_index
        self.xf_record = book.xf_list[xf_index]
        self.font = book.font_list[self.xf_record.font_index]
        self.format_rec = book.format_map[self.xf_record.format_key]

    def dxf_color(self, color_index):
        rgb = self.book.colour_map[color_index]
        if rgb:
            return color_index(rgb)
        else:
            return None

    def get_colors(self):
        bgcolor_index = self.xf_record.background.background_colour_index
        bgcolor = self.dxf_color(bgcolor_index)
        fgcolor = self.dxf_color(self.font.colour_index)
        if fgcolor is None:
            fgcolor = 7
        return fgcolor, bgcolor

    def get_textstyle(self):
        return ('STANDARD', 'TIMES', 'ARIAL')[min(self.font.family, 2)]

    def get_linespacing(self):
        return 1.5

    def get_scale(self):
        return 1.0, 1.0

    def get_textheight(self):
        return self.font.height * FONT_FACTOR

    def get_margin(self):
        return 0.1, 0.1

    def get_rotation(self):
        return 0.0

    def get_border_style(self):
        """Get border width as tuple (top, right, bottom, left).

        values: 0=none, 1=thin, 2=middle, 3=thick
        """
        def style(xf_style):
            border_style = {
                'status': True,
                'color': 5,
                'linetype': 'CONTINUOSE',
                'priority': 50,
            }
            if xf_style in [1, 3, 4, 7, 9, 11]: # thin
                border_style['color'] = 7
            elif xf_style in [2, 8, 10, 12]: # medium
                border_style['color'] = 4
            elif xf_style in [5, 6, 13]: # thick or double
                border_style['color'] = 3
            return border_style
        border = self.xf_record.border
        top = style(border.top_line_style)
        right = style(border.right_line_style)
        bottom = style(border.bottom_line_style)
        left = style(border.left_line_style)
        return (left, right, top, bottom)

    def get_align(self):
        """Get cell alignment as tuple (horiz, vert).

        horiz = 0=left, 1=center, 2=right
        vert  = 0=Baseline? 1=bottom, 2=middle, 3=top
        """
        xf_halign = self.xf_record.alignment.hor_align
        xf_valign = self.xf_record.alignment.vert_align

        halign = const.LEFT
        if xf_halign in [2, 4, 5, 6]:
            halign = const.CENTER
        elif xf_halign == 3:
            halign = const.RIGHT

        valign = const.BOTTOM
        if xf_valign == 0:
            valign = const.TOP
        elif xf_valign in [1, 3, 4]:
            valign = const.MIDDLE
        return (halign, valign)

    def tostr(self, cell):
        def float_to_string():
            def clean_format_string(fmt_str):
                if fmt_str == 'GENERAL':
                    return "0"
                fmt_str = fmt_str.split(';')[0]
                fmt_str = fmt_str.split('\\')[0]
                fmt_str = fmt_str.split(' ')[0]
                return fmt_str

            def has_thousend_point(fmt_str):
                return fmt_str.startswith('#,##')

            def get_float_prec(fmt_str):
                try:
                    return len(fmt_str) - fmt_str.rindex(FPOINT) - 1
                except ValueError:
                    return 0

            fmt_str = clean_format_string(self.format_rec.format_str)
            float_prec = get_float_prec(fmt_str)
            thousend_point = has_thousend_point(fmt_str)
            return grouped_number(cell.value, float_prec, thousend_point)

        def date_to_string(fmt_str):
            def xls_format_to_datetime_format(fmt_str):
                if 'YYYY' in fmt_str:
                    dt_fmt = '%d.%m.%Y'
                else:
                    dt_fmt = '%d.%m.%y'
                return dt_fmt

            try:
                dt = xlrd.xldate_as_tuple(cell.value, self.book.datemode)
                date = datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
            except:
                return 'DATERR'
            return date.strftime(xls_format_to_datetime_format(fmt_str))

        if cell.ctype == 1: # string
            return cell.value.encode('cp1252')
        elif cell.ctype == 4: # Boolean
            return 'True' if cell.value else 'False'
        elif cell.ctype == 5: # Error in cell
            return 'Error'
        elif cell.ctype == 2: # float
            return float_to_string()
        elif cell.ctype == 3: # date
            return date_to_string(self.format_rec.format_str)
        return ""

    def style_name(self):
        return "xf{0}".format(self.xf_index)

class SheetRenderer(object):
    def __init__(self, sheet, filename, options):
        self.sheet = sheet
        nrows = min(options.maxrows, sheet.nrows)
        ncols = min(options.maxcols, sheet.ncols)
        self.table = dxf.table((0,0), nrows, ncols)

        self.set_col_widths()
        self.set_row_heights()
        self.set_default_style()
        self.create_cell_styles()
        self.create_cells()
        self.save_dxf(filename)

    def create_cell_styles(self):
        def build_style(style, xfrec):
            halign, valign = xfrec.get_align()
            color, bg_color = xfrec.get_colors()
            textstyle = xfrec.get_textstyle()
            linespacing = xfrec.get_linespacing()
            xscale, yscale = xfrec.get_scale()
            height = xfrec.get_textheight()
            hmargin, vmargin = xfrec.get_margin()
            rotation = xfrec.get_rotation()
            left, right, top, bottom = xfrec.get_border_styles()

        for index, xf_info in enumerate(self.sheet.book.xf_list):
            xfrec = XFRecord(self.sheet.book, index)
            name = xfrec.style_name()
            style = self.table.new_cell_style(name)
            build_style(style, xf_info)

    def create_cells(self):
        for row in xrange(self.table.nrows):
            for col in xrange(self.table.ncols):
                cell = self.sheet.cell(row, col)
                if cell is xlrd.empty_cell:
                    continue
                if self.is_visible_cell(row, col):
                    span = self.get_cell_span(row, col)
                    xfrec = XFRecord(self.sheet.book, cell.xf_index)
                    style = xfrec.style_name()
                    text = xfrec.tostr(cell)
                    self.table.text_cell(row, col, text, span, style)

    def is_merged_cell(self, row, col):
        for (row_low, row_high, col_low, col_high) in self.sheet.merged_cells:
            if row==row_low and col==col_low:
                return True
        return False

    def get_cell_span(self, row, col):
        for (row_low, row_high, col_low, col_high) in self.sheet.merged_cells:
            if row==row_low and col==col_low:
                row_span = row_high - row_low + 1
                col_span = col_high - col_low + 1
        return (1, 1)

    def is_visible_cell(self, row, col):
        for (row_low, row_high, col_low, col_high) in self.sheet.merged_cells:
            if row==row_low and col==col_low:
                return True
            if row_low <= row <= row_high and \
               col_low <= col <= col_high:
                return False
        return True

    def set_default_style(self):
        pass

    def set_col_widths(self):
        def width(col):
            col_width=self.sheet.computed_column_width(col)
            return float(col_width) * WIDTH_FACTOR

        for col in xrange(self.table.ncols):
            self.table.set_col_width(col, width(col))

    def set_row_heights(self):
        def height(row):
            try:
                row_height = self.sheet.rowinfo_map[row].height
            except KeyError:
                row_heigth = self.sheet.default_row_height
            return float(row_height) * HEIGHT_FACTOR

        for row in xrange(self.table.nrows):
            self.table.set_row_height(row, height(row))

    def get_xf_record(self, row, col):
        xf_index = self.sheet.cell_xf_index(row, col)
        return self.sheet.book.xf_list[xf_index]

    def save_dxf(self, filename):
        drawing = dxf.drawing(filename)
        drawing.add(self.table)
        try:
            drawing.save()
        except IOError:
            logging.error("Unable to save dxf-file '{0}'".format(filename))
            sys.exit(1)

class Converter(object):
    def __init__(self, excel_filename, options):
        self.options = options
        try:
            self.book = xlrd.open_workbook(excel_filename, formatting_info=True)
        except IOError:
            logging.error("Unable to open excel-file '{0}'".format(excel_filename))
            sys.exit(1)

    def plot(self, sheet, dxf_filename):
        logging.info("writing dxf-file '{0}' ...".format(dxf_filename))
        SheetRenderer(sheet, dxf_filename, self.options)
        logging.info("done.")

#----------------------------------------------------------------------
def main(workbooks, options):
    def dxf_filename(workbookname, sheetname):
        return "{0}.{1}.dxf".format(workbookname.encode('cp1252'),
                                    sheetname.encode('cp1252'))
    logging.basicConfig(level=logging.INFO,
                datefmt="%Y-%m-%d, %H:%M:%S",
                format="%(asctime)s:%(levelname)s:%(message)s")
    for name_pattern in workbooks:
        for filename in glob.glob(name_pattern):
            wbname, ext = os.path.splitext(filename)
            converter = Converter(filename, options)
            if len(options.sheetname):
                try:
                    sheet = converter.book.sheet_by_name(options.sheetname)
                    converter.plot(sheet, dxf_filename(wbname, sheet.name))
                except xlrd.biffh.XLRDError:
                    logging.error("Workbook contains no sheet with name '{0}'.".format(options.sheetname))
                    sys.exit(1)
            else:
                for sheet in converter.book.sheets():
                    converter.plot(sheet, dxf_filename(wbname, sheet.name))

def get_options():
    parser = OptionParser()
    parser.add_option("-s", "--sheet", dest="sheetname", default="",
                      help="process only SHEETNAME", metavar="SHEETNAME")

    parser.add_option("-r", "--rows", dest="maxrow", type="int", default=100000,
                      help="process only first ROWS", metavar="ROWS")

    parser.add_option("-c", "--cols", dest="maxcol", type="int", default=100000,
                      help="process only first COLS", metavar="COLS")

    return parser.parse_args()

if __name__=='__main__':
    options, workbooks = get_options()
    main(workbooks, options)