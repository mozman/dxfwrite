#!/usr/bin/env python
#coding:utf-8
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.entities import Viewport
from dxfwrite import dxfstr, DXFEngine

class TestViewportEntity(unittest.TestCase):
    expected = "  0\nVIEWPORT\n  8\nVIEWPORTS\n 67\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 40\n3.0\n"\
    " 41\n2.0\n 68\n1\n 69\n1\n" \
    "1001\nACAD\n1000\nMVIEW\n1002\n{\n" \
    "1070\n16\n" \
    "1010\n0.0\n1020\n0.0\n1030\n0.0\n" \
    "1010\n0.0\n1020\n0.0\n1030\n0.0\n" \
    "1040\n0.0\n1040\n1.0\n"\
    "1040\n0.0\n1040\n0.0\n"\
    "1040\n50.0\n1040\n0.0\n1040\n0.0\n"\
    "1070\n0\n1070\n100\n1070\n1\n"\
    "1070\n3\n1070\n0\n1070\n0\n1070\n0\n1070\n0\n"\
    "1040\n0.0\n1040\n0.0\n1040\n0.0\n"\
    "1040\n0.1\n1040\n0.1\n1040\n0.1\n1040\n0.1\n"\
    "1070\n0\n"\
    "1002\n{\n1002\n}\n1002\n}\n"

    def test_create_viewport_entity(self):
        viewport = Viewport((0,0,0), 3, 2, id=1)
        self.assertEqual(dxfstr(viewport), self.expected)

    def test_viewport_by_factory(self):
        viewport = DXFEngine.viewport((0,0,0), 3, 2, id=1)
        self.assertEqual(dxfstr(viewport), self.expected)

    def test_get_extended_data(self):
        viewport = DXFEngine.viewport((0,0,0), 3, 2)
        result = viewport['perspective_lens_length']
        self.assertEqual(50, result)

    def test_set_extended_data(self):
        viewport = DXFEngine.viewport((0,0,0), 3, 2, perspective_lens_length=75.)
        result = viewport['perspective_lens_length']
        self.assertEqual(75, result)

if __name__=='__main__':
    unittest.main()
