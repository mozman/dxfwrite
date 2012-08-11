#!/usr/bin/env python
#coding:utf-8
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.tables import create_table, Viewports
from dxfwrite import dxfstr

class TestTables(unittest.TestCase):
    def test_empty_linetypes_table(self):
        table = create_table('LTYPE')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nLTYPE\n 70\n0\n  0\nENDTAB\n")

    def test_empty_layers_table(self):
        table = create_table('LAYER')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nLAYER\n 70\n0\n  0\nENDTAB\n")

    def test_contains_layer(self):
        table = create_table('LAYER')
        table.add( {'name': 'TEST'} )
        self.assertTrue('TEST' in table)

    def test_get_layer(self):
        table = create_table('LAYER')
        table.add( {'name': 'TEST'} )
        self.assertEqual(table['TEST']['name'], 'TEST')

    def test_empty_styles_table(self):
        table = create_table('STYLE')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nSTYLE\n 70\n0\n  0\nENDTAB\n")

    def test_empty_views_table(self):
        table = create_table('VIEW')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nVIEW\n 70\n0\n  0\nENDTAB\n")

    def test_empty_viewports_table(self):
        table = create_table('VPORT')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nVPORT\n 70\n0\n  0\nENDTAB\n")

    def test_empty_ucs_table(self):
        table = create_table('UCS')
        dxf = dxfstr(table)
        self.assertEqual(dxf, "  0\nTABLE\n  2\nUCS\n 70\n0\n  0\nENDTAB\n")

    def test_tables_error(self):
        self.assertRaises(ValueError, create_table, 'ERROR')

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

    def test_get_tables_with_same_names(self):
        vport = Viewports()
        vport.add(self.table1)
        vport.add(self.table2)
        self.assertEqual(len(vport['test']), 2)

        
if __name__=='__main__':
    unittest.main()
