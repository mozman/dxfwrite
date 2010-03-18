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
DEFAULT_CELL_VALIGN = const.BOTTOM
DEFAULT_CELL_TEXT_COLOR = const.BYLAYER
DEFAULT_CELL_BG_COLOR = None
DEFAULT_BORDER_COLOR = 5
DEFAULT_BORDER_LINETYPE = None
DEFAULT_BORDER_STATUS = True
DEFAULT_BORDER_MARGIN = 0.1

BORDER_LEFT = 0
BORDER_TOP = 1
BORDER_RIGHT = 2
BORDER_BOTTOM = 3

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
        Set <border> (BORDER_LEFT, ...) to given values.

        Arguments
        ---------
        status -- if True border will be drawn
        color -- dxf color index
        linetype -- linetype name, BYLAYER if None
        margin -- distance to entity in drawing units
        """
        style = Style._get_default_border_style()
        style.update(kwargs)
        self['borders'][border] = style

    @staticmethod
    def _get_default_cell_style():
        return Style({
            'textstyle': 'STANDARD',
            'textheight': DEFAULT_CELL_TEXT_HEIGHT,
            'linespacing': DEFAULT_CELL_LINESPACING,
            'xscale': DEFAULT_CELL_XSCALE,
            'yscale': DEFAULT_CELL_YSCALE,
            'textcolor': DEFAULT_CELL_TEXT_COLOR,
            'rotation' : 0.,
            'halign': DEFAULT_CELL_HALIGN,
            'valign': DEFAULT_CELL_VALIGN,
            'bgcolor': DEFAULT_CELL_BG_COLOR,
            'borders': [
                Style._get_default_border_style(), # BORDER_LEFT
                Style._get_default_border_style(), # BORDER_TOP
                Style._get_default_border_style(), # BORDER_RIGHT
                Style._get_default_border_style(), # BORDER_BOTTOM
                ],
        })

    @staticmethod
    def _get_default_border_style():
        return {
            'status': DEFAULT_BORDER_STATUS,
            'color': DEFAULT_BORDER_COLOR,
            'linetype': DEFAULT_BORDER_LINETYPE,
            'margin': DEFAULT_BORDER_MARGIN,
        }

class Table(object):
    def __init__(self, insert, nrows, ncols):
        self.insert = insert
        self.nrows = nrows
        self.ncols = ncols
        self.rowheight = [DEFAULT_TABLE_HEIGHT] * nrows
        self.colwidth = [DEFAULT_TABLE_WIDTH] * ncols
        self.bglayer = DEFAULT_TABLE_BGLAYER
        self.fglayer = DEFAULT_TABLE_FGLAYER
        self.gridlayer = DEFAULT_TABLE_GRIDLAYER
        self.styles = {'default': Style._get_default_cell_style()}
        self.cells = {}
        self.cell_visible_map = None # created in _build_table
        self.data = DXFList() # dxf entities

    def textcell(self, row, col, text, style='default'):
        cell = TextCell(self.styles[style], text)
        self.cells[row, col] = cell
        return cell

    def blockcell(self, row, col, blockdef, attribs={}, style=None):
        cell = BlockCell(style if style else self.default_style, blockdef, attribs)
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
        self.data = DXFList() #
        return result


    def _build_table(self):
        pass

class Cell(object):
    def __init__(self, style):
        self.style = style
        self.span = (1, 1)

    def get_dxf_entity(self, insert, layer):
        raise NotImplementedError()

class TextCell(Cell):
    def __init__(self, style, text):
        super(TextCell, self).__init__(style)
        self.text = text

    def get_dxf_entity(self, pos, layer):
        return MText(self.text, pos,
                     linespacing=self.style.linespacing,
                     style=self.style.textstyle,
                     heigth=self.style.textheight,
                     rotation=self.style.rotation,
                     xscale=self.style.xscale,
                     halign=self.style.halign,
                     valign=self.style.valign,
                     color=self.style.textcolor,
                     layer=layer)

class BlockCell(Cell):
    def __init__(self, style, blockdef, attribs={}):
        super(BlockCell, self).__init__(style)
        self.blockdef = blockdef # dxf block definition!
        self.attribs = attribs

    def get_dxf_entities(self, pos, layer):
        insert = Insert(insert=pos, layer=layer)
