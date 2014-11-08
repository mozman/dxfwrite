#!/usr/bin/env python
#coding:utf-8
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.tableentries import View
from dxfwrite import dxfstr, DXFEngine

class TestViewTableEntry(unittest.TestCase):
    expected = "  0\nVIEW\n  2\nTest\n 70\n0\n 40\n1.0\n 41\n1.0\n 10\n" \
                 "0.5\n 20\n0.5\n 11\n0.0\n 21\n0.0\n 31\n1.0\n 12\n0.0\n 22\n" \
                 "0.0\n 32\n0.0\n 42\n50.0\n 43\n0.0\n 44\n0.0\n 50\n0.0\n 71\n0\n"

    def test_create_table_entry(self):
        view = View('Test')
        self.assertEqual(dxfstr(view), self.expected)

    def test_view_by_factory(self):
        view = DXFEngine.view('Test')
        self.assertEqual(dxfstr(view), self.expected)

if __name__=='__main__':
    unittest.main()
