#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.buildups.MText
# Created: 09.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest2 as unittest

from dxfwrite.mtext import MText
import dxfwrite

class TestMText(unittest.TestCase):

    def setUp(self):
        self.addTypeEqualityFunc(str, self.assertMultiLineEqual)
        self.expected_line = "  0\nTEXT\n 62\n256\n  8\n0\n 10\n{point[0]}\n 20\n{point[1]}\n" \
            " 30\n{point[2]}\n 40\n1.0\n  1\n{text}\n 50\n0.0\n" \
            " 41\n1.0\n 51\n0.0\n  7\nSTANDARD\n 71\n0\n 72\n0\n 73\n{valign}\n" \
            " 11\n{point[0]}\n 21\n{point[1]}\n 31\n{point[2]}\n"

        self.expected_line_rot = "  0\nTEXT\n 62\n256\n  8\n0\n 10\n{point[0]}\n 20\n{point[1]}\n" \
            " 30\n{point[2]}\n 40\n1.0\n  1\n{text}\n 50\n{rot}\n" \
            " 41\n1.0\n 51\n0.0\n  7\nSTANDARD\n 71\n0\n 72\n0\n 73\n{valign}\n" \
            " 11\n{point[0]}\n 21\n{point[1]}\n 31\n{point[2]}\n"

    def test_horiz_top(self):
        text = "lineA\nlineB"
        valign = dxfwrite.TOP
        mtext = MText(text, (0., 0., 0.), 1.0)
        line1 = self.expected_line.format(text='lineA', point=(0., 0., 0.), valign=valign)
        line2 = self.expected_line.format(text='lineB', point=(0.,-1., 0.), valign=valign)
        self.assertEqual(mtext.__dxf__(), line1+line2)

    def test_horiz_bottom(self):
        text = "lineA\nlineB"
        valign = dxfwrite.BOTTOM
        mtext = MText(text, (0., 0., 0.), 1.0, valign=valign)
        line1 = self.expected_line.format(text='lineA', point=(0., 1., 0.), valign=valign)
        line2 = self.expected_line.format(text='lineB', point=(0., 0., 0.), valign=valign)
        self.assertEqual(mtext.__dxf__(), line1+line2)

    def test_horiz_middle(self):
        text = "lineA\nlineB"
        valign = dxfwrite.MIDDLE
        mtext = MText(text, (0., 0., 0.), 1.0, valign=valign)
        line1 = self.expected_line.format(text='lineA', point=(0., 0.5, 0.), valign=valign)
        line2 = self.expected_line.format(text='lineB', point=(0., -.5, 0.), valign=valign)
        self.assertEqual(mtext.__dxf__(), line1+line2)

    def test_45deg_top(self):
        text = "lineA\nlineB\nlineC"
        valign = dxfwrite.TOP
        rotation = 45.
        mtext = MText(text, (0., 0., 0.), 1.0, rotation=rotation)
        line1 = self.expected_line_rot.format(text='lineA', point=(0., 0., 0.),
                                              valign=valign, rot=rotation)
        line2 = self.expected_line_rot.format(text='lineB', point=(+.707107, -.707107, 0.),
                                              valign=valign, rot=rotation)
        line3 = self.expected_line_rot.format(text='lineC', point=(+1.414214, -1.414214, 0.),
                                              valign=valign, rot=rotation)

        self.assertEqual(mtext.__dxf__(), line1+line2+line3)

    def test_45deg_bottom(self):
        text = "lineA\nlineB\nlineC"
        valign = dxfwrite.BOTTOM
        rotation = 45.
        mtext = MText(text, (0., 0., 0.), 1.0, valign=valign, rotation=rotation)
        line1 = self.expected_line_rot.format(text='lineA', point=(-1.414214, +1.414214, 0.),
                                              valign=valign, rot=rotation)
        line2 = self.expected_line_rot.format(text='lineB', point=(-.707107, +.707107, 0.),
                                              valign=valign, rot=rotation)
        line3 = self.expected_line_rot.format(text='lineC', point=(0., 0., 0.),
                                              valign=valign, rot=rotation)

        self.assertEqual(mtext.__dxf__(), line1+line2+line3)

if __name__=='__main__':
    unittest.main()