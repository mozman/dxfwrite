#!/usr/bin/env python
#coding:utf-8
# Purpose: test dxfwrite.entities.Arc
# Created: 20.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import dxfstr
from dxfwrite.entities import Arc

class TestArc(unittest.TestCase):
    def test_arc_no_attributes(self):
        arc = Arc()
        expected = "  0\nARC\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 40\n1.0\n 50\n0.0\n 51\n360.0\n"
        self.assertEqual(dxfstr(arc), expected)

    def test_arc_with_attribs(self):
        arc = Arc(center=(1,1), radius=1, startangle=30, endangle=60)
        expected = "  0\nARC\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n 40\n1.0\n 50\n30.0\n 51\n60.0\n"
        self.assertEqual(dxfstr(arc), expected)

if __name__=='__main__':
    unittest.main()
