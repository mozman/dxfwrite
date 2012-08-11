#!/usr/bin/env python
#coding:utf-8
# Created: 22.02.2010
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

from dxfwrite.entities import Polyline
from dxfwrite import dxfstr

class TestPolyline(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(str, self.assertMultiLineEqual)

    def test_polyline(self):
        polyline = Polyline()
        polyline.add_vertex( (0, 0) )
        vt1 = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n"
        polyline.add_vertex( (1, 1) )
        vt2 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n"
        expected = "  0\nPOLYLINE\n  8\n0\n 66\n1\n 10\n0.0\n 20\n0.0\n 30\n0.0\n" \
                 " 70\n8\n" + vt1 + vt2 + "  0\nSEQEND\n"
        self.assertEqual(dxfstr(polyline), expected)

    def test_invalid_polyline(self):
        polyline = Polyline()
        self.assertFalse(polyline.valid())


if __name__=='__main__':
    unittest.main()
