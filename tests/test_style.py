#!/usr/bin/env python
#coding:utf-8
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.tableentries import Style
from dxfwrite import dxfstr, DXFEngine

class TestStyleTableEntry(unittest.TestCase):
    expected = "  0\nSTYLE\n  2\nARIAL\n 70\n0\n 40\n0.0\n 41\n1.0\n 42\n1.0\n 50\n" \
               "75.0\n 71\n4\n  3\nArial.ttf\n  4\n\n"
    def set_params(self, style):
        style['oblique'] = 75
        style['generation_flags'] = 4

    def test_create_table_entry(self):
        style = Style("ARIAL", font='Arial.ttf')
        self.set_params(style)
        self.assertEqual(dxfstr(style), self.expected)

    def test_style_by_factory(self):
        style = DXFEngine.style("ARIAL",
                              font='Arial.ttf')
        self.set_params(style)
        self.assertEqual(dxfstr(style), self.expected)

if __name__=='__main__':
    unittest.main()
