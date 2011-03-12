#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.buildups.MText
# Created: 09.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
if sys.version_info[:2]> (2, 6):
    import unittest
else: # python 2.6 and prior needs the unittest2 package
    import unittest2 as unittest

from string import Template

from dxfwrite.mtext import MText
import dxfwrite

class TestMText(unittest.TestCase):
    expected_line = Template("  0\nTEXT\n 62\n256\n  8\n0\n 10\n${px}\n 20\n${py}\n" \
                             " 30\n${pz}\n 40\n1.0\n  1\n${text}\n 50\n0.0\n" \
                             " 41\n1.0\n 51\n0.0\n  7\nSTANDARD\n 71\n0\n 72\n0\n 73\n${valign}\n" \
                             " 11\n${px}\n 21\n${py}\n 31\n${pz}\n")
    expected_line_rot = Template("  0\nTEXT\n 62\n256\n  8\n0\n 10\n${px}\n 20\n${py}\n" \
                                 " 30\n${pz}\n 40\n1.0\n  1\n${text}\n 50\n${rot}\n" \
                                 " 41\n1.0\n 51\n0.0\n  7\nSTANDARD\n 71\n0\n 72\n0\n 73\n${valign}\n" \
                                 " 11\n${px}\n 21\n${py}\n 31\n${pz}\n")

    def setUp(self):
        self.addTypeEqualityFunc(str, self.assertMultiLineEqual)

    def test_horiz_top(self):
        text = "lineA\nlineB"
        valign = dxfwrite.TOP
        mtext = MText(text, (0., 0., 0.), 1.0)
        line1 = self.expected_line.substitute(text='lineA', px='0.0', py='0.0', pz='0.0', valign=str(valign))
        line2 = self.expected_line.substitute(text='lineB', px='0.0', py='-1.0', pz='0.0', valign=str(valign))
        self.assertEqual(mtext.__dxf__(), line1+line2)

    def test_horiz_bottom(self):
        text = "lineA\nlineB"
        valign = dxfwrite.BOTTOM
        mtext = MText(text, (0., 0., 0.), 1.0, valign=valign)
        line1 = self.expected_line.substitute(text='lineA', px='0.0', py='1.0', pz='0.0', valign=str(valign))
        line2 = self.expected_line.substitute(text='lineB', px='0.0', py='0.0', pz='0.0', valign=str(valign))
        self.assertEqual(mtext.__dxf__(), line1+line2)

    def test_baseline(self):
        mtext = MText("lineA\nlineB", (0., 0., 0.), 1.0, valign=dxfwrite.BASELINE)
        self.assertEqual(mtext.valign, dxfwrite.BOTTOM)

    def test_horiz_middle(self):
        text = "lineA\nlineB"
        valign = dxfwrite.MIDDLE
        mtext = MText(text, (0., 0., 0.), 1.0, valign=valign)
        line1 = self.expected_line.substitute(text='lineA', px='0.0', py='0.5', pz='0.0', valign=str(valign))
        line2 = self.expected_line.substitute(text='lineB', px='0.0', py='-0.5', pz='0.0', valign=str(valign))
        self.assertEqual(mtext.__dxf__(), line1+line2)

    def test_45deg_top(self):
        text = "lineA\nlineB\nlineC"
        valign = dxfwrite.TOP
        rotation = 45.
        mtext = MText(text, (0., 0., 0.), 1.0, rotation=rotation)
        line1 = self.expected_line_rot.substitute(text='lineA', px='0.0', py='0.0', pz='0.0',
                                              valign=str(valign), rot=str(rotation))
        line2 = self.expected_line_rot.substitute(text='lineB', px='0.707107', py='-0.707107', pz='0.0',
                                              valign=str(valign), rot=str(rotation))
        line3 = self.expected_line_rot.substitute(text='lineC', px='1.414214', py='-1.414214', pz='0.0',
                                              valign=str(valign), rot=str(rotation))

        self.assertEqual(mtext.__dxf__(), line1+line2+line3)

    def test_45deg_bottom(self):
        text = "lineA\nlineB\nlineC"
        valign = dxfwrite.BOTTOM
        rotation = 45.
        mtext = MText(text, (0., 0., 0.), 1.0, valign=valign, rotation=rotation)
        line1 = self.expected_line_rot.substitute(text='lineA', px='-1.414214', py='1.414214', pz='0.0',
                                              valign=str(valign), rot=str(rotation))
        line2 = self.expected_line_rot.substitute(text='lineB', px='-0.707107', py='0.707107', pz='0.0',
                                              valign=str(valign), rot=str(rotation))
        line3 = self.expected_line_rot.substitute(text='lineC', px='0.0', py='0.0', pz='0.0',
                                              valign=str(valign), rot=str(rotation))

        self.assertEqual(mtext.__dxf__(), line1+line2+line3)

if __name__=='__main__':
    unittest.main()