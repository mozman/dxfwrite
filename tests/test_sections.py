#!/usr/bin/env python
#coding:utf-8
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import *
from dxfwrite.sections import create_section

class TestSection(unittest.TestCase):

    def test_empty_header_section(self):
        dxf = dxfstr(create_section('HEADER'))
        self.assertTrue(dxf.startswith("  0\nSECTION\n  2\nHEADER\n"))
        self.assertTrue(dxf.endswith("\n  0\nENDSEC\n"))

    def test_empty_entities_section(self):
        dxf = dxfstr(create_section('ENTITIES'))
        self.assertTrue(dxf.startswith("  0\nSECTION\n  2\nENTITIES\n"))
        self.assertTrue(dxf.endswith("\n  0\nENDSEC\n"))

    def test_empty_blocks_section(self):
        dxf = dxfstr(create_section('BLOCKS'))
        self.assertTrue(dxf.startswith("  0\nSECTION\n  2\nBLOCKS\n"))
        self.assertTrue(dxf.endswith("\n  0\nENDSEC\n"))

    def test_empty_tables_section(self):
        dxf = dxfstr(create_section('TABLES'))
        self.assertTrue(dxf.startswith("  0\nSECTION\n  2\nTABLES\n"))
        self.assertTrue(dxf.endswith("\n  0\nENDSEC\n"))

    def test_header_vars_point_3d(self):
        header = create_section('HEADER')
        header['$EXTMIN'] = (0, 0, 0)
        header['$EXTMAX'] = (99, 117, 0)
        extmax = header['$EXTMAX']
        self.assertEqual(extmax[0], 99)
        self.assertEqual(extmax[1], 117)
        self.assertEqual(extmax[2], 0)
        dxf = dxfstr(header)
        self.assertTrue('  9\n$EXTMIN\n 10\n0.0\n 20\n0.0\n 30\n0.0\n' in dxf)
        self.assertTrue('  9\n$EXTMAX\n 10\n99.0\n 20\n117.0\n 30\n0.0\n' in dxf)

    def test_header_vars_string(self):
        header = create_section('HEADER')
        header['$ACADVER'] = 'AC1009'
        dxf = dxfstr(header)
        self.assertTrue('  9\n$ACADVER\n  1\nAC1009\n' in dxf)

    def test_header_vars_float(self):
        header = create_section('HEADER')
        header['$ANGBASE'] = 30
        dxf = dxfstr(header)
        self.assertTrue('  9\n$ANGBASE\n 50\n30.0\n' in dxf)

    def test_get_section_error(self):
        self.assertRaises(ValueError, create_section, 'MOZMAN')


if __name__=='__main__':
    unittest.main()
