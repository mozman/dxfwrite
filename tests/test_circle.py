#!/usr/bin/env python
#coding:utf-8
# Created: 20.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

import unittest

from dxfwrite.base import dxfstr
from dxfwrite.entities import Circle

class TestCircle(unittest.TestCase):
    def test_circle_no_attributes(self):
        circle = Circle()
        expected = "  0\nCIRCLE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 40\n1.0\n"
        self.assertEqual(dxfstr(circle), expected)

    def test_circle_2d_center(self):
        circle = Circle(center=(0,0), radius=1)
        expected = "  0\nCIRCLE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 40\n1.0\n"
        self.assertEqual(dxfstr(circle), expected)

if __name__=='__main__':
    unittest.main()
