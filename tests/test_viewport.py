#!/usr/bin/env python
#coding:utf-8
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.tableentries import VPort
from dxfwrite import dxfstr, DXFEngine

class TestViewportTableEntry(unittest.TestCase):
    expected = "  0\nVPORT\n  2\nTest\n 70\n" \
             "0\n 10\n0.0\n 20\n0.0\n 11\n1.0\n 21\n1.0\n 12\n0.5\n 22\n" \
             "0.5\n 13\n0.0\n 23\n0.0\n 14\n0.1\n 24\n0.1\n 15\n0.1\n 25\n" \
             "0.1\n 16\n0.0\n 26\n0.0\n 36\n1.0\n 17\n0.0\n 27\n0.0\n 37\n" \
             "0.0\n 42\n50.0\n 43\n0.0\n 44\n0.0\n 40\n1.0\n 41\n1.0\n 50\n" \
             "0.0\n 51\n0.0\n 68\n0\n 69\n0\n 71\n0\n 72\n100\n 73\n1\n 74\n" \
             "3\n 75\n0\n 76\n0\n 77\n0\n 78\n0\n"

    def test_create_table_entry(self):
        viewport = VPort('Test')
        self.assertEqual(dxfstr(viewport), self.expected)

    def test_vport_by_factory(self):
        viewport = DXFEngine.vport('Test')
        self.assertEqual(dxfstr(viewport), self.expected)


if __name__=='__main__':
    unittest.main()
