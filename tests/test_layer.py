#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.tablentries.layer
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest

from dxfwrite.tableentries import Layer
from dxfwrite import dxfstr, DXFEngine


class TestLayerTableEntry(unittest.TestCase):
    expected = "  0\nLAYER\n  2\nStandard\n 70\n0\n 62\n1\n  6\nCONTINUOUS\n"
    def test_create_table_entry(self):
        layer = Layer('Standard', linetype='CONTINUOUS')
        self.assertEqual(dxfstr(layer), self.expected)

    def test_layer_by_factory(self):
        layer = DXFEngine.layer('Standard', linetype='CONTINUOUS')
        self.assertEqual(dxfstr(layer), self.expected)

if __name__=='__main__':
    unittest.main()