#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.tables
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest

from dxfwrite.tables import Tables, Viewports
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

    def test_contains_layer(self):
        table = Tables().get('LAYER')
        table.add( {'name': 'TEST'} )
        self.assertTrue('TEST' in table)

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

    def test_tables_error(self):
        self.assertRaises(ValueError, Tables.get, 'ERROR')

class TestViewPorts(unittest.TestCase):
    table1 = {'name': 'test'}
    table2 = {'name': 'test'}
    def test_tables_with_same_names(self):
        vport = Viewports()
        vport.add(self.table1)
        vport.add(self.table2)
        count = 0
        for table in vport._get_values():
            count += 1
            self.assertEqual(table['name'], 'test')
        self.assertEqual(count, 2)
if __name__=='__main__':
    unittest.main()