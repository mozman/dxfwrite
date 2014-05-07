#!/usr/bin/env python
#coding:utf-8
# Created: 20.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import dxfstr, DXFValidationError
from dxfwrite.entities import Face3D

class TestFace3D(unittest.TestCase):
    def test_face3d_no_attributes(self):
        face3d = Face3D() # need at least 3 points
        self.assertRaises( DXFValidationError, dxfstr, face3d)
        face3d = Face3D( [(0,0)] ) # need at least 3 points
        self.assertRaises( DXFValidationError, dxfstr, face3d )
        face3d = Face3D( [(0,0), (1,0)] ) # need at least 3 points
        self.assertRaises( DXFValidationError, dxfstr, face3d )

    def test_face3d_3points(self):
        face3d = Face3D( [(0,0), (1,0), (1,1)] )
        expected = "  0\n3DFACE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n0.0\n 31\n0.0\n" \
                 " 12\n1.0\n 22\n1.0\n 32\n0.0\n 13\n1.0\n 23\n1.0\n 33\n0.0\n"
        self.assertEqual(dxfstr(face3d), expected)

    def test_face3d_4points(self):
        face3d = Face3D( [(0,0), (1,0), (1,1), (0,1)] )
        expected = "  0\n3DFACE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n0.0\n 31\n0.0\n" \
                 " 12\n1.0\n 22\n1.0\n 32\n0.0\n 13\n0.0\n 23\n1.0\n 33\n0.0\n"
        self.assertEqual(dxfstr(face3d), expected)

    def test_face3d_flags(self):
        face3d = Face3D( [(0,0), (1,0), (1,1), (0,1)], flags=1 )
        expected = "  0\n3DFACE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n0.0\n 31\n0.0\n" \
                 " 12\n1.0\n 22\n1.0\n 32\n0.0\n 13\n0.0\n 23\n1.0\n 33\n0.0\n 70\n1\n"
        self.assertEqual(dxfstr(face3d), expected)

    def test_face3d_change_point(self):
        face3d = Face3D( [(0,0), (1,0), (1,1), (0,1)] )
        face3d[3] = (0, 2) # tuple! not DXFPoint
        expected = "  0\n3DFACE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n0.0\n 31\n0.0\n" \
                 " 12\n1.0\n 22\n1.0\n 32\n0.0\n 13\n0.0\n 23\n2.0\n 33\n0.0\n"
        self.assertEqual(dxfstr(face3d), expected)


if __name__=='__main__':
    unittest.main()
