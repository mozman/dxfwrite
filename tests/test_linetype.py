#!/usr/bin/env python
#coding:utf-8
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.tableentries import Linetype
from dxfwrite import DXFEngine, dxfstr

class TestLinetypeTableEntry(unittest.TestCase):
    pattern = Linetype.make_line_pattern_definition([0.6, 0.5, -0.1])
    expected = "  0\nLTYPE\n  2\nDASHED\n 70\n0\n  3\nstrichliert\n%s" % dxfstr(pattern)
    def test_linepattern(self):
        expected = " 72\n65\n 73\n2\n 40\n0.6\n" \
                   " 49\n0.5\n 49\n-0.1\n"
        self.assertEqual(dxfstr(self.pattern), expected)

    def test_create_table_entry(self):
        ltype = Linetype('DASHED',
                         description="strichliert",
                         pattern=self.pattern)

        self.assertEqual(dxfstr(ltype), self.expected)

    def test_create_table_entry_by_factory(self):
        ltype = DXFEngine.linetype('DASHED',
                         description="strichliert",
                         pattern=self.pattern)

        self.assertEqual(dxfstr(ltype), self.expected)

if __name__=='__main__':
    unittest.main()
