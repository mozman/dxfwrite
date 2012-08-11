#!/usr/bin/env python
#coding:utf-8
# Created: 20.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import dxfstr
from dxfwrite.entities import Point

class TestPoint(unittest.TestCase):
    def test_circle_no_attributes(self):
        point = Point()
        expected = "  0\nPOINT\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n"
        self.assertEqual(dxfstr(point), expected)

    def test_point_with_attribs(self):
        point = Point(point=(1,1), orientation=-1)
        expected = "  0\nPOINT\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n 50\n-1.0\n"
        self.assertEqual(dxfstr(point), expected)

if __name__=='__main__':
    unittest.main()
