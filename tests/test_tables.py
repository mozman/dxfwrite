#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.tables
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest

from dxfwrite.tables import *
from dxfwrite import dxfstr

class TestTables(unittest.TestCase):
    def test_empty_linetypes_table(self):
        table = Tables().get('LTYPE')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nLTYPE\n 70\n0\n  0\nENDTAB\n")
    def test_empty_layers_table(self):
        table = Tables().get('LAYER')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nLAYER\n 70\n0\n  0\nENDTAB\n")
    def test_empty_styles_table(self):
        table = Tables().get('STYLE')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nSTYLE\n 70\n0\n  0\nENDTAB\n")
    def test_empty_views_table(self):
        table = Tables().get('VIEW')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nVIEW\n 70\n0\n  0\nENDTAB\n")
    def test_empty_viewports_table(self):
        table = Tables().get('VPORT')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nVPORT\n 70\n0\n  0\nENDTAB\n")
    def test_empty_ucs_table(self):
        table = Tables().get('UCS')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nUCS\n 70\n0\n  0\nENDTAB\n")

if __name__=='__main__':
    unittest.main()