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

# http://www.lexicon.net/sjmachin/xlrd.htm
import xlrd
# http://bitbucket.org/mozman/dxfwrite
import dxfwrite.const as const
from dxfwrite import DXFEngine as dxf
from dxfwrite.std import color_index

locale.setlocale(locale.LC_ALL, "")

HAIR   = 5 # 0.13
THIN   = 7 # 0.25
MEDIUM = 4 # 0.50
THICK  = 3 # 0.70
HEIGHT_FACTOR = 0.001763671
WIDTH_FACTOR = 0.000764724
FONT_FACTOR = HEIGHT_FACTOR * 0.7
FPOINT = '.'
MAX_FLOAT_PREC = 6
HIDDEN = (0, 0)

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

    def dxf_color(self, cindex):
        rgb = self.book.colour_map[cindex]
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
        return 0.1, 0.05

    def is_stacked_text(self):
        return self.xf_record.alignment.rotation == 255

    def get_rotation(self):
        if self.is_stacked_text():
            return 0.
        rotation = self.xf_record.alignment.rotation
        if 90 < rotation <= 180:
            rotation = -(rotation - 90)
        return rotation

    def get_border_styles(self):
        """Returns a tuple of border styles.
        """
        def style(xf_style):
            border_style = {
                'status': True,
                'color': 5,
                'linetype': 'CONTINUOUS',
                'priority': 50,
            }
            # set color = line width
            if xf_style == 0: # no line
                border_style['status'] = False
                border_style['priority'] = 50
            elif xf_style == 7: # hair OpenOffice = 0.05 pt
                border_style['color'] = HAIR
                border_style['priority'] = 60
            elif xf_style in [1, 3, 4, 9, 11]: # thin OpenOffice = 0.5 & 1.0 pt
                border_style['color'] = THIN
                border_style['priority'] = 70
            elif xf_style in [2, 8, 10, 12]: # medium OpenOffice = 2.5 pt
                border_style['color'] = MEDIUM
                border_style['priority'] = 80
            elif xf_style in [5, 6, 13]: # thick or double OpenOffice = 4.0 pt
                border_style['color'] = THICK
                border_style['priority'] = 90
            return border_style
        border = self.xf_record.border
        top = style(border.top_line_style)
        right = style(border.right_line_style)
        bottom = style(border.bottom_line_style)
        left = style(border.left_line_style)
        return (left, right, top, bottom)

    def get_align(self):
        """Get cell alignment as tuple (halign, valign).

        halign -- LEFT, CENTER, RIGHT from const module
        valign -- TOP, MIDDLE, BOTTM from const module
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

class VisibilityMap(object):
    """Stores the visibility of table cells."""
    def __init__(self, sheet):
        """Constructor

        sheet -- excel sheet from xlrd
        """
        self._merged_cells = dict()
        self._create_visibility_map(sheet)

    def _create_visibility_map(self, sheet):
        """Set visibility for all merged cells."""
        for cell_range in sheet.merged_cells:
            self._set_span_visibility(cell_range)

    def _set_span_visibility(self, cell_range):
        """Set the visibilty of the given cell. The top-left cell itself is
        visible, all other cells in the cell-range are invisible, they are c
        overed by the top-left cell."""
        row_lo, row_hi, col_lo, col_hi = cell_range
        # set all cells in span range to HIDDEN
        for rowx in xrange(row_lo, row_hi):
            for colx in xrange(col_lo, col_hi):
                self._merged_cells[rowx, colx] = HIDDEN

        # set span-tuple value of the merged cell (top_left)
        self._merged_cells[row_lo, col_lo] = (row_hi-row_lo, col_hi-col_lo)

    def is_visible(self, row, col):
        """Get visibility status of indexd cell; index is a tuple:<row>, <col>.
        returns False for hidden or True for visible
        """
        return self.get_cell_span(row, col) != HIDDEN

    def get_cell_span(self, row, col):
        try:
            return self._merged_cells[row, col]
        except KeyError: # not a merged cell
            return (1, 1)

class SheetRenderer(object):
    def __init__(self, sheet, filename, options):
        self.sheet = sheet
        nrows = min(options.maxrow, sheet.nrows)
        ncols = min(options.maxcol, sheet.ncols)
        self.table = dxf.table((0,0), nrows, ncols)
        self.xfrecords= []
        self.vismap = VisibilityMap(sheet)

        self.set_col_widths()
        self.set_row_heights()
        self.set_default_style()
        self.create_cell_styles()
        self.create_cells()
        self.save_dxf(filename)

    def create_cell_styles(self):
        def build_style(style, xfrec):
            style['halign'], style['valign'] = xfrec.get_align()
            style['textcolor'], style['bgcolor'] = xfrec.get_colors()
            style['textstyle'] = xfrec.get_textstyle()
            style['textheight'] = xfrec.get_textheight()
            style['linespacing'] = xfrec.get_linespacing()
            style['xscale'], style['yscale'] = xfrec.get_scale()
            style['hmargin'], style['vmargin'] = xfrec.get_margin()
            style['rotation'] = xfrec.get_rotation()
            style['stacked'] = xfrec.is_stacked_text()
            style['left'], style['right'], style['top'], style['bottom'] = xfrec.get_border_styles()

        for index, xf_info in enumerate(self.sheet.book.xf_list):
            xfrec = XFRecord(self.sheet.book, index)
            self.xfrecords.append(xfrec)
            name = xfrec.style_name()
            style = self.table.new_cell_style(name)
            build_style(style, xfrec)

    def create_cells(self):
        for row in xrange(self.table.nrows):
            for col in xrange(self.table.ncols):
                if self.vismap.is_visible(row, col):
                    cell = self.sheet.cell(row, col)
                    xfrec = self.xfrecords[cell.xf_index]
                    text = xfrec.tostr(cell)
                    span = self.vismap.get_cell_span(row, col)
                    style = xfrec.style_name()
                    self.table.text_cell(row, col, text, span, style)

    def set_default_style(self):
        default_style = self.table.get_cell_style('default')
        # now modify the default style

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
                row_height = self.sheet.default_row_height
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