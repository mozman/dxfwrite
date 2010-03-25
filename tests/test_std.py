#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.acadctb
# Created: 25.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import unittest2 as unittest

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
    def test_init(self):
        colors = DXFColorIndex()
        self.assertTrue(colors is not None)

    def test_get_rgb(self):
        colors = DXFColorIndex()
        self.assertEqual(colors.get_rgb(1), (255, 0, 0))

    def test_get_nearest_color(self):
        colors = DXFColorIndex()
        self.assertEqual(colors.get_dxf_color_index((254, 1, 1)), 1)

    def test_index_range(self):
        colors = DXFColorIndex()
        self.assertRaises(IndexError, colors.get_rgb, 0)
        self.assertRaises(IndexError, colors.get_rgb, 256)

    def test_user_styles(self):
        styles = UserStylesMock()
        colors = DXFColorIndex(user_styles=styles)
        self.assertEqual(colors.get_rgb(DXF_INDEX), TESTCOLOR)
        NEAR_COLOR = (TESTCOLOR[0]-3, TESTCOLOR[1]+1, TESTCOLOR[2]+1)
        self.assertEqual(colors.get_dxf_color_index(NEAR_COLOR), DXF_INDEX)

if __name__=='__main__':
    unittest.main()