#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: table, consisting of basic R12 entities
# module belongs to package: dxfwrite.py
# Created: 18.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3
"""
A spreadsheet like table, but without calculations, buildup with
DXF R12 entities.
"""
from array import array
from copy import deepcopy

import dxfwrite.const as const
from dxfwrite.base import DXFList
from dxfwrite.entities import Line, Solid, Insert
from dxfwrite.buildups import MText

__all__ = ['Table', 'CustomCell']

DEFAULT_TABLE_BGLAYER = 'TABLEBACKGROUND'
DEFAULT_TABLE_FGLAYER = 'TABLECONTENT'
DEFAULT_TABLE_GRIDLAYER = 'TABLEGRID'
DEFAULT_TABLE_BGLAYER = 'BACKGROUND'
DEFAULT_TABLE_HEIGHT = 1.0
DEFAULT_TABLE_WIDTH  = 2.5
DEFAULT_TEXTSTYLE = 'STANDARD'
DEFAULT_CELL_TEXT_HEIGHT = 0.7
DEFAULT_CELL_LINESPACING = 1.5
DEFAULT_CELL_XSCALE = 1.0
DEFAULT_CELL_YSCALE = 1.0
DEFAULT_CELL_HALIGN = const.LEFT
DEFAULT_CELL_VALIGN = const.TOP
DEFAULT_CELL_TEXTCOLOR = const.BYLAYER
DEFAULT_CELL_BG_COLOR = None
DEFAULT_CELL_HMARGIN = 0.1
DEFAULT_CELL_VMARGIN = 0.1
DEFAULT_BORDER_COLOR = 5
DEFAULT_BORDER_LINETYPE = None
DEFAULT_BORDER_STATUS = True
DEFAULT_BORDER_PRIORITY = 50

VISIBLE = 1
HIDDEN = 0

class Table(object):
    def __init__(self, insert, nrows, ncols, default_grid=True):
        self.insert = insert
        self.nrows = nrows
        self.ncols = ncols
        self.row_heights = [DEFAULT_TABLE_HEIGHT] * nrows
        self.col_widths = [DEFAULT_TABLE_WIDTH] * ncols
        self.bglayer = DEFAULT_TABLE_BGLAYER
        self.fglayer = DEFAULT_TABLE_FGLAYER
        self.gridlayer = DEFAULT_TABLE_GRIDLAYER
        self.styles = {'default': Style.get_default_cell_style()}
        if not default_grid:
            default_style = self.get_cell_style('default')
            default_style.set_border_status(False, False, False, False)
        self.cells = {}
        self.frames = []
        self.visibility_map = None # created in _setup
        self.grid = None # manage the border lines, created in _setup
        self.data = DXFList() # dxf entities
        self.empty_cell = Cell(self)

    def set_col_width(self, column, value):
        self.col_widths[column] = float(value)

    def set_row_height(self, row, value):
        self.row_heights[row] = float(value)

    def text_cell(self, row, col, text, span=(1, 1), style='default'):
        cell = TextCell(self, text, style=style, span=span)
        self.cells[row, col] = cell
        return cell

    def block_cell(self, row, col, blockdef, span=(1, 1), attribs={}, style='default'):
        cell = BlockCell(self, blockdef, style=style, attribs=attribs, span=span)
        self.cells[row, col] = cell
        return cell

    def custom_cell(self, row, col, custom_cell):
        self.cells[row, col] = custom_cell
        return custom_cell

    def frame(self, row, col, width=1, height=1, style='default'):
        frame = Frame(self, pos=(row, col), span=(height, width),
                      style=style)
        self.frames.append(frame)
        return frame

    def new_cell_style(self, name, **kwargs):
        style = deepcopy(self.get_cell_style('default'))
        style.update(kwargs)
        self.styles[name] = style
        return style

    def new_border_style(self, color=const.BYLAYER, status=True,
                         priority=100, linetype=None):
        border_style = Style.get_default_border_style()
        border_style['color'] = color
        border_style['linetype'] = linetype
        border_style['status'] = status
        border_style['priority'] = priority
        return border_style

    def get_cell_style(self, name):
        return self.styles[name]

    def cell(self, row, col):
        try:
            return self.cells[(row, col)]
        except KeyError:
            return self.empty_cell # emtpy cell with default style

    def iter_visible_cells(self):
        return ((row, col, self.cell(row, col)) for row, col in self.visibility_map)

    @property
    def name(self):
        """ entitiy type name """
        return 'TABLE'

    def __dxf__(self):
        self._build_table()
        result = self.data.__dxf__()
        self.data = DXFList() # don't need to keep this data in memory
        return result

    def _setup(self):
        self.visibility_map = VisibilityMap(self, status=VISIBLE)
        self.grid = Grid(self)

    def _build_table(self):
        self._setup()
        self.grid.draw()
        for row, col, cell in self.iter_visible_cells():
            self.grid.draw_background(row, col, cell)
            self.grid.draw_content(row, col, cell)
        self._cleanup()

    def _cleanup(self):
        self.visibility_map = None
        self.grid = None

class VisibilityMap(object):
    def __init__(self, table, status):
        self.table = table
        self._cells = array('B', (status for _ in xrange(self.table.nrows*self.table.ncols)))
        self._create_visibility_map()

    def _create_visibility_map(self):
        for row, col in iter(self):
            cell = self.table.cell(row, col)
            self._set_span_visibility(row, col, cell.span)

    def _set_span_visibility(self, row, col, span):
        if span == (1, 1):
            return
        for rowx in xrange(span[0]):
            for colx in xrange(span[1]):
                # switch all cells in span range to invisible
                self.hide(row+rowx, col+colx)
        # switch content cell visible
        self.show(row, col)

    def _get_index(self, row, col):
        return row*self.table.ncols+col

    def get(self, row, col):
        return self._cells[self._get_index(row, col)]

    def show(self, row, col):
        self._cells[self._get_index(row, col)] = VISIBLE

    def hide(self, row, col):
        self._cells[self._get_index(row, col)] = HIDDEN

    def iter_all_cells(self):
        for row in xrange(self.table.nrows):
            for col in xrange(self.table.ncols):
                yield (row, col)

    def is_visible_cell(self, row, col):
        return self.get(row, col) == VISIBLE

    def __iter__(self):
        """ iterate over all visible cells """
        return ( (row, col) for (row, col) in self.iter_all_cells() \
                 if self.is_visible_cell(row, col) )

class Style(dict):
    @staticmethod
    def get_default_cell_style():
        return Style({
            'textstyle': 'STANDARD',
            'textheight': DEFAULT_CELL_TEXT_HEIGHT,
            'linespacing': DEFAULT_CELL_LINESPACING,
            'xscale': DEFAULT_CELL_XSCALE,
            'yscale': DEFAULT_CELL_YSCALE,
            'textcolor': DEFAULT_CELL_TEXTCOLOR,
            'rotation' : 0.,
            'halign': DEFAULT_CELL_HALIGN,
            'valign': DEFAULT_CELL_VALIGN,
            'hmargin': DEFAULT_CELL_HMARGIN,
            'vmargin': DEFAULT_CELL_VMARGIN,
            'bgcolor': DEFAULT_CELL_BG_COLOR,
            'left': Style.get_default_border_style(),
            'top': Style.get_default_border_style(),
            'right': Style.get_default_border_style(),
            'bottom': Style.get_default_border_style(),
        })

    @staticmethod
    def get_default_border_style():
        return {
            'status': DEFAULT_BORDER_STATUS,
            'color': DEFAULT_BORDER_COLOR,
            'linetype': DEFAULT_BORDER_LINETYPE,
            'priority': DEFAULT_BORDER_PRIORITY,
        }

    def set_border_status(self, left=True, right=True, top=True, bottom=True):
        for border, status in (('left', left),
                               ('right', right),
                               ('top', top),
                               ('bottom', bottom)):
            self[border]['status'] = status

    def set_border_style(self, style,
                         left=True, right=True, top=True, bottom=True):
        for border, status in (('left', left),
                               ('right', right),
                               ('top', top),
                               ('bottom', bottom)):
            if status:
                self[border] = style

class Grid(object):
    def __init__(self, table):
        self.table = table
        self.col_pos = self._calc_col_pos()
        self.row_pos = self._calc_row_pos()
        self._hborders = {}
        self._vborders = {}
        self.default_border_style = Style.get_default_border_style()

    def _init_borders(self, rows, cols, border):
        for row in xrange(rows+1):
            for col in xrange(cols+1):
                self._hborders[(row, col)] = border
                self._vborders[(row, col)] = border

    def set_hborder(self, row, col, border_style):
        return self._set_border_style(self._hborders, row, col, border_style)

    def set_vborder(self, row, col, border_style):
        return self._set_border_style(self._vborders, row, col, border_style)

    def _set_border_style(self, borders, row, col, border_style):
        try:
            actual_borderstyle = borders[(row, col)]
            if border_style['priority'] >= actual_borderstyle['priority']:
                borders[(row, col)] = border_style
        except KeyError:
            borders[(row, col)] = border_style

    def _sum_fields(self, start_value, fields, append, sign=1.):
        position = start_value
        append(position)
        for element in fields:
            position += element * sign
            append(position)

    def _calc_col_pos(self):
        # col_pos contains the x-axis for the cells
        # for cell[i]: left = col_pos[i], rigth = row_pos[i+colspan]
        col_pos = array('f')
        self._sum_fields(self.table.insert[0],
                         self.table.col_widths,
                         col_pos.append)
        return col_pos

    def _calc_row_pos(self):
        # row_pos contains the y-axis for the cells
        # for cell[i]: top = row_pos[i], bottom = row_pos[i+rowspan]
        row_pos = array('f')
        self._sum_fields(self.table.insert[1],
                         self.table.row_heights,
                         row_pos.append, -1.)
        return row_pos

    def cell_coords(self, row, col, span):
        """ Get the coordinates of the given cell. """
        top = self.row_pos[row]
        bottom = self.row_pos[row+span[0]]
        left = self.col_pos[col]
        right = self.col_pos[col+span[1]]
        return (left, right, top, bottom)

    def draw_background(self, row, col, cell):
        """ Draw the cell background as DXF-SOLID entity. """
        style = cell.style
        if style['bgcolor'] is None:
            return
        left, right, top, bottom = self.cell_coords(row, col, cell.span)
        ltop = (left, top)
        lbot = (left, bottom)
        rtop = (right, top)
        rbot = (right, bottom)
        self.table.data.append(Solid(
            points=[ltop, lbot, rbot, rtop],
            color=style['bgcolor'],
            layer=self.table.bglayer))

    def draw_content(self, row, col, cell):
        """ Draw the cell content, calls the cell method get_dxf_entity to
        create the cell content.
        """
        coords = self.cell_coords(row, col, cell.span)
        dxf_entity = cell.get_dxf_entity(coords, self.table.fglayer)
        self.table.data.append(dxf_entity)

    def draw(self):
        """ Draw the whole grid lines. """
        noborder = Style.get_default_border_style()
        noborder['status'] = HIDDEN
        noborder['priority'] = 0
        self._init_borders(self.table.nrows, self.table.ncols, noborder)
        self._set_frames(self.table.frames)
        # set frame borders before cell borders, so _set_borders can remove
        # frame borders inside of cell span regions - not implemented yet
        self._set_borders(self.table.iter_visible_cells())
        self._draw_borders(self.table)

    def _set_borders(self, visible_cells):
        """ Set borders to style values of all visible cells. """
        for row, col, cell in visible_cells:
            bottom_row = row + cell.span[0]
            right_col = col + cell.span[1]
            self._set_rect_border(row, bottom_row, col, right_col, cell.style)

    def _set_rect_border(self, top_row, bottom_row, left_col, right_col, style):
        for col in xrange(left_col, right_col):
            self.set_hborder(top_row, col, style['top'])
            self.set_hborder(bottom_row, col, style['bottom'])
        for row in xrange(top_row, bottom_row):
            self.set_vborder(row, left_col, style['left'])
            self.set_vborder(row, right_col, style['right'])

    def _set_frames(self, frames):
        """ Set borders for all defined frames. """
        for frame in frames:
            top_row = frame.pos[0]
            left_col = frame.pos[1]
            bottom_row = top_row + frame.span[0]
            right_col = left_col + frame.span[1]
            self._set_rect_border(top_row, bottom_row, left_col, right_col,
                                  frame.style)

    def _draw_borders(self, table):
        """ Draws the grid lines as DXF-LINE entities. """
        def append_line(start, end, style):
            """ Appends the DXF-LINE entity to the table dxf data. """
            if style['status']:
                table.data.append(Line(
                    start=start,
                    end=end,
                    layer=layer,
                    color=style['color'],
                    linetype=style['linetype']))

        def draw_hborders():
            """ Draws the horizontal lines. """
            for row in xrange(table.nrows+1):
                yrow = self.row_pos[row]
                for col in xrange(table.ncols):
                    xleft = self.col_pos[col]
                    xright = self.col_pos[col+1]
                    style = self._hborders[row, col]
                    append_line((xleft, yrow), (xright, yrow), style)

        def draw_vborders():
            """ Draws the vertical l ines """
            for col in xrange(table.ncols+1):
                xcol = self.col_pos[col]
                for row in xrange(table.nrows):
                    ytop = self.row_pos[row]
                    ybottom = self.row_pos[row+1]
                    style = self._vborders[row, col]
                    append_line((xcol, ytop), (xcol, ybottom), style)

        layer = table.gridlayer
        draw_hborders()
        draw_vborders()

class Frame(object):
    def __init__(self, table, pos=(0, 0), span=(1 ,1), style='default'):
        self.table = table
        self.pos = pos
        self.span = span
        self.stylename = style

    @property
    def style(self):
        return self.table.get_cell_style(self.stylename)

class Cell(object):
    @property
    def span(self): # pylint: disable-msg=E0202
        return self._span
    @span.setter # pylint: disable-msg=E1101
    def span(self, value): # pylint: disable-msg=E0102,E0202
        self._span = (max(1, value[0]), max(1, value[1]))

    def __init__(self, table, style='default', span=(1, 1)):
        self.table = table
        self.stylename = style
        # span values has to have >= 1
        self.span = span

    def get_dxf_entity(self, coords, layer):
        return DXFList()

    def substract_margin(self, coords):
        hmargin = self.style['hmargin']
        vmargin = self.style['vmargin']
        return ( coords[0]+hmargin, # left
                 coords[1]-hmargin, # right
                 coords[2]-vmargin, # top
                 coords[3]+vmargin ) # bottom
    @property
    def style(self):
        return self.table.get_cell_style(self.stylename)

class TextCell(Cell):
    """ Cell that contains a multiline text. """
    def __init__(self, table,  text, style='default', span=(1, 1)):
        super(TextCell, self).__init__(table, style, span)
        self.text = text

    def get_dxf_entity(self, coords, layer):
        if len(self.text) == 0:
            return DXFList()
        left, right, top, bottom = self.substract_margin(coords)
        style = self.style
        halign = style['halign']
        valign = style['valign']
        xpos = (left, float(left+right)/2., right)[halign]
        ypos = (bottom, float(bottom+top)/2., top)[valign-1]
        return MText(self.text, (xpos, ypos),
                     linespacing=self.style['linespacing'],
                     style=self.style['textstyle'],
                     height=self.style['textheight'],
                     rotation=self.style['rotation'],
                     xscale=self.style['xscale'],
                     halign=halign,
                     valign=valign,
                     color=self.style['textcolor'],
                     layer=layer)

class CustomCell(Cell):
    """ Cell with 'user' controlled content. """
    def __init__(self, table, style='default', span=(1, 1)):
        super(CustomCell, self).__init__(table, style, span)

    def get_dxf_entity(self, coords, layer):
        """ override this methode and create an arbitrary dxf element

        coords -- tuple of border-coordinates : left, right, top, bottom
        layer -- layer, which should be used for dxf entities
        """
        style = self.style # access to all the parameter
        # reduce borders about hmargin and vmargin
        left, right, top, bottom = self.substract_margin(coords)
        # and now do what you want ...
        # return a dxf entity which implement the __dxf__ protocoll
        # DXFList is a good choice
        raise NotImplementedError()


class BlockCell(Cell):
    """ Cell that contains a block reference. """
    def __init__(self, table, blockdef, style='default', attribs={}, span=(1, 1)):
        super(BlockCell, self).__init__(table, style, span)
        self.blockdef = blockdef # dxf block definition!
        self.attribs = attribs

    def get_dxf_entity(self, coords, layer):
        left, right, top, bottom = self.substract_margin(coords)
        style = self.style
        halign = style['halign']
        valign = style['valign']
        xpos = (left, float(left+right)/2., right)[halign]
        ypos = (bottom, float(bottom+top)/2., top)[valign-1]
        insert = Insert(blockname=self.blockdef['name'],
                        insert=(xpos, ypos),
                        xscale=style['xscale'],
                        yscale=style['yscale'],
                        rotation=style['rotation'],
                        layer=layer)
        # process attribs
        for key, value in self.attribs.iteritems():
            attdef = self.blockdef.find_attdef(key)
            attrib = attdef.new_attrib(text=value)
            insert.add(attrib, relative=True)
        return insert
