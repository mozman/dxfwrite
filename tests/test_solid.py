#!/usr/bin/env python
#coding:utf-8
# Created: 20.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import dxfstr, DXFValidationError
from dxfwrite.entities import Solid

class TestSolid(unittest.TestCase):
    def test_solid_no_attributes(self):
        solid = Solid() # need at least 3 points
        self.assertRaises( DXFValidationError, dxfstr, solid)
        solid = Solid( [(0,0)] ) # need at least 3 points
        self.assertRaises( DXFValidationError, dxfstr, solid )
        solid = Solid( [(0,0), (1,0)] ) # need at least 3 points
        self.assertRaises( DXFValidationError, dxfstr, solid )

    def test_solid_3points(self):
        solid = Solid( [(0,0), (1,0), (1,1)] )
        expected = "  0\nSOLID\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n0.0\n 31\n0.0\n" \
                 " 13\n1.0\n 23\n1.0\n 33\n0.0\n 12\n1.0\n 22\n1.0\n 32\n0.0\n"
        self.assertEqual(dxfstr(solid), expected)

    def test_solid_4points(self):
        solid = Solid( [(0,0), (1,0), (1,1), (0,1)] )
        expected = "  0\nSOLID\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n0.0\n 31\n0.0\n" \
                 " 13\n1.0\n 23\n1.0\n 33\n0.0\n 12\n0.0\n 22\n1.0\n 32\n0.0\n"
        self.assertEqual(dxfstr(solid), expected)

    def test_solid_change_point(self):
        solid = Solid( [(0,0), (1,0), (1,1), (0,1)] )
        solid[3] = (0, 2) # tuple! not DXFPoint
        expected = "  0\nSOLID\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n0.0\n 31\n0.0\n" \
                 " 13\n1.0\n 23\n1.0\n 33\n0.0\n 12\n0.0\n 22\n2.0\n 32\n0.0\n"
        self.assertEqual(dxfstr(solid), expected)


if __name__=='__main__':
    unittest.main()
