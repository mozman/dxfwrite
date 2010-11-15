#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.sections.Sections
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest

from dxfwrite.base import *
from dxfwrite.sections import Sections
from dxfwrite.tables import Tables

class TestSection(unittest.TestCase):

    def test_empty_header_section(self):
        dxf = dxfstr(Sections.get('HEADER'))
        self.assertTrue(dxf.startswith("  0\nSECTION\n  2\nHEADER\n"))
        self.assertTrue(dxf.endswith("\n  0\nENDSEC\n"))

    def test_empty_entities_section(self):
        dxf = dxfstr(Sections.get('ENTITIES'))
        self.assertTrue(dxf.startswith("  0\nSECTION\n  2\nENTITIES\n"))
        self.assertTrue(dxf.endswith("\n  0\nENDSEC\n"))

    def test_empty_blocks_section(self):
        dxf = dxfstr(Sections.get('BLOCKS'))
        self.assertTrue(dxf.startswith("  0\nSECTION\n  2\nBLOCKS\n"))
        self.assertTrue(dxf.endswith("\n  0\nENDSEC\n"))

    def test_empty_tables_section(self):
        dxf = dxfstr(Sections.get('TABLES'))
        self.assertTrue(dxf.startswith("  0\nSECTION\n  2\nTABLES\n"))
        self.assertTrue(dxf.endswith("\n  0\nENDSEC\n"))

    def test_header_point_vars(self):
        header = Sections.get('HEADER')
        header.add('$EXTMIN', DXFPoint())
        header.add('$EXTMAX', DXFPoint( (99, 117, 0) ))
        extmax = header.get('$EXTMAX')
        self.assertEqual(extmax[0], 99)
        self.assertEqual(extmax[1], 117)
        self.assertEqual(extmax[2], 0)
        dxf = dxfstr(header)
        self.assertTrue('  9\n$EXTMIN\n 10\n0.0\n 20\n0.0\n 30\n0.0\n' in dxf)
        self.assertTrue('  9\n$EXTMAX\n 10\n99.0\n 20\n117.0\n 30\n0.0\n' in dxf)

    def test_get_section_error(self):
        self.assertRaises(ValueError, Sections.get, 'MOZMAN')


if __name__=='__main__':
    unittest.main()