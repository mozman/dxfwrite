#!/usr/bin/env python
#coding:utf-8
# Created: 25.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

try:
    # Python 2.6 and earlier need the unittest2 package
    # try: easy_install unittest2
    # or download source from: http://pypi.python.org/pypi/unittest2
    import unittest2 as unittest
except ImportError:
    import unittest

from dxfwrite.std import *

TESTLW = 0.37
TESTCOLOR = (123, 23, 33)
DXF_INDEX = 7

class UserStylesMock(object):
    def get_color(self, dxf_color_index):
        if dxf_color_index == DXF_INDEX:
            return TESTCOLOR
        else:
            return None

    def get_lineweight(self, dxf_color_index):
        if dxf_color_index == DXF_INDEX:
            return TESTLW
        else:
            return None

class TestDXFLineweight(unittest.TestCase):
    def test_init(self):
        lineweights = DXFLineweight()
        self.assertTrue(lineweights is not None)

    def test_get_dxf_standard(self):
        lineweights = DXFLineweight(LW_DXF)
        self.assertAlmostEqual(lineweights.get(1), 1.40)

    def test_get_iso_standard(self):
        lineweights = DXFLineweight(LW_ISO)
        self.assertAlmostEqual(lineweights.get(1), 0.50)

    def test_index_range(self):
        lineweights = DXFLineweight()
        self.assertRaises(IndexError, lineweights.get, 0)
        self.assertRaises(IndexError, lineweights.get, 256)

    def test_with_user_styles(self):
        styles = UserStylesMock()
        lineweights = DXFLineweight(user_styles=styles)
        self.assertAlmostEqual(lineweights.get(DXF_INDEX), TESTLW)

class TestDXFColorIndex(unittest.TestCase):
    def setUp(self):
        self.colors = DXFColorIndex()

    def test_init(self):
        self.assertTrue(self.colors is not None)

    def test_get_rgb(self):
        self.assertEqual(self.colors.get_rgb(1), (255, 0, 0))

    def test_get_black(self):
        # stupid special case black/white == 7
        self.assertEqual(self.colors.get_dxf_color_index( (0, 0, 0) ), 7)

    def test_get_white(self):
        # stupid special case black/white == 7
        self.assertEqual(self.colors.get_dxf_color_index( (255, 255, 255) ), 7)

    def test_black_color_name_to_dxf_index(self):
        self.assertEqual(7, self.colors.get_dxf_color_index_by_colorname('black'))

    def test_white_color_name_to_dxf_index(self):
        # stupid dxf black/white == 7 issue
        self.assertEqual(7, self.colors.get_dxf_color_index_by_colorname('white'))

    def test_get_nearest_color(self):
        self.assertEqual(self.colors.get_dxf_color_index((254, 1, 1)), 1)

    def test_index_range(self):
        self.assertRaises(IndexError, self.colors.get_rgb, 0)
        self.assertRaises(IndexError, self.colors.get_rgb, 256)

    def test_user_styles(self):
        styles = UserStylesMock()
        colors = DXFColorIndex(user_styles=styles)
        self.assertEqual(colors.get_rgb(DXF_INDEX), TESTCOLOR)
        NEAR_COLOR = (TESTCOLOR[0]-3, TESTCOLOR[1]+1, TESTCOLOR[2]+1)
        self.assertEqual(colors.get_dxf_color_index(NEAR_COLOR), DXF_INDEX)

if __name__=='__main__':
    unittest.main()
