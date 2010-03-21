#!/usr/bin/env python
#coding:utf-8
# test module ray2d.py
# Author:  mozman
# Purpose: test Table - a buildup of basic dxf entities
# Created: 21.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest2 as unittest
from itertools import izip

from dxfwrite.table import Table, DEFAULT_CELL_TEXTCOLOR, CustomCell
from dxfwrite.table import Grid

class DXFMock:
    counter = 0
    def __dxf__(self):
        DXFMock.counter += 1
        return ""

class TestCell(CustomCell):
    counter = 0
    def get_dxf_entity(self, coords, layer):
        TestCell.counter += 1
        return DXFMock()

class TestTableApi(unittest.TestCase):
    def test_init(self):
        table = Table((0, 0), 10, 10, default_grid=False)
        self.assertTrue(bool(table))
        style = table.get_cell_style('default')
        for border in ['left', 'right', 'top', 'bottom']:
            self.assertFalse(style[border]['status'])

        table = Table((0, 0), 10, 10, default_grid=True)
        style = table.get_cell_style('default')
        for border in ['left', 'right', 'top', 'bottom']:
            self.assertTrue(style[border]['status'])

    def test_name(self):
        table = Table((0, 0), 10, 10)
        self.assertEqual(table.name, 'TABLE')

    def test_setter_methods(self):
        table = Table((0, 0), 10, 10)
        table.set_col_width(0, 3.)
        self.assertEqual(table.col_widths[0], 3.)
        table.set_row_height(0, 4.)
        self.assertEqual(table.row_heights[0], 4.)

    def test_cell_index(self):
        table = Table((0, 0), 10, 10)
        self.assertRaises(IndexError, table.get_cell, 10, 10)
        self.assertRaises(IndexError, table.get_cell, -1, 10)

    def test_default_text_cell(self):
        table = Table((0, 0), 10, 10)
        table.text_cell(0, 0, 'test')
        cell = table.get_cell(0, 0)
        self.assertEqual(cell.span, (1, 1))
        self.assertEqual(cell.text, 'test')
        self.assertEqual(cell.stylename, 'default')

    def test_text_cell(self):
        table = Table((0, 0), 10, 10)
        table.text_cell(8, 8, 'test88', span=(2, 2), style='extrastyle')
        cell = table.get_cell(8, 8)
        self.assertEqual(cell.span, (2, 2))
        self.assertEqual(cell.text, 'test88')
        self.assertEqual(cell.stylename, 'extrastyle')

    def test_block_cell(self):
        table = Table((0, 0), 10, 10)
        table.block_cell(1, 1, None, span=(3, 3))
        cell = table.get_cell(1, 1)
        self.assertEqual(cell.span, (3, 3))
        self.assertEqual(cell.blockdef, None)
        self.assertEqual(cell.stylename, 'default')

    def test_frame(self):
        table = Table((0, 0), 10, 10)
        frame = table.frame(0, 0, width=10, height=2)
        self.assertEqual(frame.pos, (0, 0))
        self.assertEqual(frame.span, (2, 10))

    def test_cell_style(self):
        table = Table((0, 0), 10, 10)
        style = table.new_cell_style('extra', textcolor=199)
        style = table.get_cell_style('extra')
        self.assertEqual(style['textcolor'], 199)
        self.assertRaises(KeyError, table.get_cell_style, 'extraextra')

    def test_border_style(self):
        table = Table((0, 0), 10, 10)
        border_style = table.new_border_style(color=1, status=True,
                                              linetype='DOT', priority=99)
        self.assertDictEqual(border_style, {'color':1,
                                            'status': True,
                                            'linetype': 'DOT',
                                            'priority': 99})

class TestTableImplementation(unittest.TestCase):
    def test_visibility_map(self):
        table = Table((0, 0), 3, 3)
        textcell = table.text_cell(0, 0, 'text', span=(2,2))
        table._setup() # creates the visibilty_map
        empty = table.empty_cell
        expected = [(0, 0, textcell), (0, 2, empty), # cell (0, 1) is covered by (0,0)
                    (1, 2, empty), # cells (1, 0), (1, 2) are coverd by cell (0, 0)
                    (2, 0, empty), (2, 1, empty), (2, 2, empty)] #row 2
        for got, should in izip(table.iter_visible_cells(), expected):
            self.assertEqual(got[0], should[0]) # row
            self.assertEqual(got[1], should[1]) # col
            self.assertEqual(got[2], should[2]) # cell

    def test_dxf_creation(self):
        self.reset_counter()
        table = Table((0, 0), 3, 3)
        indices = [(0, 0), (0, 1), (0, 2),
                   (1, 0), (1, 1), (1, 2),
                   (2, 0), (2, 1), (2, 2)]
        cell = TestCell(table, 'default', (1, 1))
        for row, col in indices:
            table.set_cell(row, col, cell)
        table.__dxf__()
        dxfmock = DXFMock()
        self.assertEqual(cell.counter, 9) # count get_dxf_entity calls
        self.assertEqual(cell.counter, dxfmock.counter)

    def reset_counter(self):
        DXFMock.counter = 0
        TestCell.counter = 0

    def test_dxf_creation_span(self):
        self.reset_counter()
        table = Table((0, 0), 3, 3)
        indices = [(0, 0), (0, 1), (0, 2),
                   (1, 0), (1, 1), (1, 2),
                   (2, 0), (2, 1), (2, 2)]
        cell = TestCell(table, 'default', (1, 1))
        for row, col in indices:
            table.set_cell(row, col, cell)
        spancell = TestCell(table, 'default', span=(2, 2)) # hides 3 cells
        table.set_cell(0, 0, spancell)
        table.__dxf__()
        dxfmock = DXFMock()
        self.assertEqual(cell.counter, 6) # count get_dxf_entity calls
        self.assertEqual(cell.counter, dxfmock.counter)

    def test_span_beyond_table_borders(self):
        table = Table((0, 0), 3, 3)
        table.text_cell(0, 2, "ERROR", span=(1, 2))
        self.assertRaises(IndexError, table.__dxf__)
        table.text_cell(2, 0, "ERROR", span=(2, 1))
        self.assertRaises(IndexError, table.__dxf__)

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.table = Table((0, 0), 3, 3)
        for x in xrange(3):
            self.table.set_col_width(x, 3.0)
            self.table.set_row_height(x, 3.0)

    def test_grid_coords(self):
        grid = Grid(self.table)
        left, right, top, bottom = grid.cell_coords(1, 1, span=(1, 1))
        self.assertAlmostEqual(left, 3., 4)
        self.assertAlmostEqual(right, 6., 4)
        self.assertAlmostEqual(top, -3., 4)
        self.assertAlmostEqual(bottom, -6., 4)

    def test_grid_coords_span(self):
        grid = Grid(self.table)
        left, right, top, bottom = grid.cell_coords(0, 0, span=(2, 2))
        self.assertAlmostEqual(left, 0., 4)
        self.assertAlmostEqual(right, 6., 4)
        self.assertAlmostEqual(top, 0., 4)
        self.assertAlmostEqual(bottom, -6., 4)

if __name__ == '__main__':
    unittest.main()
