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

import dxfwrite.const as const
from dxfwrite.base import DXFList
from dxfwrite.entities import Line, Solid, Insert
from dxfwrite.buildups import MText

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


class CellMap(object):
    def __init__(self, nrows, ncols, default=1):
        self.nrows = nrows
        self.ncols = ncols
        self._cells = array('B', (default for _ in xrange(nrows*ncols)))

    def _get_index(self, row, col):
        return row*self.ncols+col

    def get(self, row, col):
        return self._cells[self._get_index(row, col)]

    def set(self, row, col, value):
        self._cells[self._get_index(row, col)] = value

class Style(dict):
    def set_border_style(self, border, **kwargs):
        """
        Set <border> ('left', ...) to given values.

        Arguments
        ---------
        status -- if True border will be drawn
        color -- dxf color index
        linetype -- linetype name, BYLAYER if None
        """
        style = Style._get_default_border_style()
        style.update(kwargs)
        self[border] = style

    @staticmethod
    def _get_default_cell_style():
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
            'left': Style._get_default_border_style(),
            'top': Style._get_default_border_style(),
            'right': Style._get_default_border_style(),
            'bottom': Style._get_default_border_style(),
        })

    @staticmethod
    def _get_default_border_style():
        return {
            'status': DEFAULT_BORDER_STATUS,
            'color': DEFAULT_BORDER_COLOR,
            'linetype': DEFAULT_BORDER_LINETYPE,
        }

class Table(object):
    def __init__(self, insert, nrows, ncols):
        self.insert = insert
        self.nrows = nrows
        self.ncols = ncols
        self.rowheights = [DEFAULT_TABLE_HEIGHT] * nrows
        self.colwidths = [DEFAULT_TABLE_WIDTH] * ncols
        self.bglayer = DEFAULT_TABLE_BGLAYER
        self.fglayer = DEFAULT_TABLE_FGLAYER
        self.gridlayer = DEFAULT_TABLE_GRIDLAYER
        self.styles = {'default': Style._get_default_cell_style()}
        self.cells = {}
        self.visibility_map = None # created in _build_table
        self.data = DXFList() # dxf entities

    def textcell(self, row, col, text, stylename='default'):
        cell = TextCell(self, stylename, text)
        self.cells[row, col] = cell
        return cell

    def blockcell(self, row, col, blockdef, attribs={}, stylename='default'):
        cell = BlockCell(self, stylename, blockdef, attribs)
        self.cells[row, col] = cell
        return cell

    def new_cellstyle(self, name, **kwargs):
        style = Style._get_default_cell_style()
        style.update(kwargs)
        self.styles[name] = style
        return style

    def get_cellstyle(self, name):
        return self.styles[name]

    @property
    def name(self):
        """ entitiy type name """
        return 'TABLE'

    def __dxf__(self):
        self._build_table()
        result = self.data.__dxf__()
        self.data = DXFList() # don't need to keep this data in memory
        return result

    def _set_span_visibility(self, row, col, span):
        if span == (1, 1) : return
        for rowx in xrange(span[0]):
            for colx in xrange(span[1]):
                # switch all cells in span range to invisible
                self.visibility_map.set(row+rowx, col+colx, 0)
        # switch content cell visible
        self.visibility_map.set(row, col, 1)

    def _iter_cells(self):
        for row in xrange(self.nrows):
            for col in xrange(self.ncols):
                yield (row, col)

    def _iter_visible_cells(self):
        return ( (row, col) for (row, col) in self._iter_cells() \
                 if self.is_visible_cell(row, col) )

    def is_visible_cell(self, row, col):
        return bool(self.visibility_map.get(row, col))

    def _create_visibility_map(self):
        self.visibility_map = CellMap(self.nrows, self.ncols, 1)
        for row, col in self._iter_visible_cells():
            cell = self.cells.get( (row, col) )
            if cell is not None:
                self._set_span_visibility(row, col, cell.span)

    def _sum_fields(self, fields, append, sign=1.):
        position = 0.
        append(position)
        for element in fields:
            position += element * sign
            append(position)

    def _calc_col_pos(self):
        # _col_pos contains the x-axis for the cells
        # for cell[i]: left = _col_pos[i], rigth = _row_pos[i+colspan]
        self._col_pos = array('f')
        self._sum_fields(self.colwidths, self._col_pos.append)

    def _calc_row_pos(self):
        # _row_pos contains the y-axis for the cells
        # for cell[i]: top = _row_pos[i], bottom = _row_pos[i+rowspan]
        self._row_pos = array('f')
        self._sum_fields(self.rowheights, self._row_pos.append, -1.)

    def _get_cell_coords(self, row, col, span):
        top = self._row_pos[row]
        bottom = self._row_pos[row+span[0]]
        left = self._col_pos[col]
        right = self._col_pos[col+span[1]]
        return (left, right, top, bottom)

    def _setup(self):
        self._create_visibility_map()
        self._calc_col_pos()
        self._calc_row_pos()

    def _build_table(self):
        self._setup()
        for row, col in self._iter_visible_cells():
            cell = self.cells.get( (row, col) )
            if cell:
                span = cell.span
                style = cell.style
            else:
                span = (1, 1)
                style = self.get_cellstyle('default')
            coords = self._get_cell_coords(row, col, span)
            self._draw_border(coords, style, self.gridlayer)
            self._draw_background(coords, style, self.bglayer)
            if cell:
                self.data.append(cell.get_dxf_entity(coords, self.fglayer))

    def _draw_border(self, coords, style, layer):
        left, right, top, bottom = coords
        ltop = (left, top)
        lbot = (left, bottom)
        rtop = (right, top)
        rbot = (right, bottom)
        for start, end, border_style in (
            (ltop, lbot, style['left']),
            (lbot, rbot, style['bottom']),
            (rbot, rtop, style['right']),
            (rtop, ltop, style['top'])):
            if border_style['status'] is True:
                self.data.append(Line(
                    start=start,
                    end=end,
                    layer=layer,
                    color=border_style['color'],
                    linetype=border_style['linetype']))

    def _draw_background(self, coords, style, layer):
        if style['bgcolor'] is None:
            return
        left, right, top, bottom = coords
        ltop = (left, top)
        lbot = (left, bottom)
        rtop = (right, top)
        rbot = (right, bottom)
        self.data.append(Solid(points=[ltop, lbot, rbot, rtop],
                               color=style['bgcolor'],
                               layer=layer))

class Cell(object):
    def __init__(self, table, stylename, span):
        self.table=table
        self.stylename = stylename
        # span values has to have >= 1
        self.span = span

    @property
    def span(self):
        return self._span
    @span.setter
    def span(self, value):
        self._span = (max(1, value[0]), max(1, value[1]))

    def get_dxf_entity(self, coords, layer):
        raise NotImplementedError()

    def substract_margin(self, coords):
        hmargin = self.style['hmargin']
        vmargin = self.style['vmargin']
        return ( coords[0]+hmargin, # left
                 coords[1]-hmargin, # right
                 coords[2]-vmargin, # top
                 coords[3]+vmargin ) # bottom
    @property
    def style(self):
        return self.table.get_cellstyle(self.stylename)


class TextCell(Cell):
    def __init__(self, table, stylename, text, span=(1, 1)):
        super(TextCell, self).__init__(table, stylename, span)
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

class BlockCell(Cell):
    def __init__(self, table, stylename, blockdef, attribs={}):
        raise NotImplemented()
        #super(BlockCell, self).__init__(table, stylename)
        #self.blockdef = blockdef # dxf block definition!
        #self.attribs = attribs

    def get_dxf_entity(self, coords, layer):
        pass
        #left, right, top, bottom = coords
        #insert = Insert(insert=(left, top), layer=layer)
        #return insert
