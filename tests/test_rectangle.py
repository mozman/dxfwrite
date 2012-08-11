#!/usr/bin/env python
#coding:utf-8
# Created: 22.03.2010
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

import dxfwrite
from dxfwrite.helpers import normalize_dxf_chunk
from dxfwrite.base import dxfstr

from dxfwrite.rect import Rectangle

class TestRectangleAPI(unittest.TestCase):
    def test_init(self):
        rect = Rectangle(
            insert=(0, 0),
            width=5,
            height=3,
            rotation=45,
            halign=dxfwrite.CENTER,
            valign=dxfwrite.MIDDLE,
            color=2,
            bgcolor=3,
            layer='RECTANGLE',
            linetype="DASHED")
        dxf = dxfstr(rect)
        self.assertTrue("DASHED" in dxf)
        self.assertTrue("RECTANGLE" in dxf)

class TestRectangleImplementation(unittest.TestCase):
    def test_components(self):
        expected = "  0\nPOLYLINE\n 62\n256\n  8\nRECTANGLE\n 66\n1\n 10\n"\
                 "0.0\n 20\n0.0\n 30\n0.0\n 70\n9\n  0\nVERTEX\n  8\n0\n 10\n"\
                 "0.0\n 20\n0.0\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n"\
                 "3.53553390593\n 20\n3.53553390593\n 30\n0.0\n  0\nVERTEX\n"\
                 "  8\n0\n 10\n1.41421356237\n 20\n5.65685424949\n 30\n0.0\n"\
                 "  0\nVERTEX\n  8\n0\n 10\n-2.12132034356\n 20\n2.12132034356\n"\
                 " 30\n0.0\n  0\nSEQEND\n  0\nSOLID\n 62\n3\n  8\nRECTANGLE\n"\
                 " 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n3.53553390593\n 21\n"\
                 "3.53553390593\n 31\n0.0\n 13\n1.41421356237\n 23\n"\
                 "5.65685424949\n 33\n0.0\n 12\n-2.12132034356\n 22\n"\
                 "2.12132034356\n 32\n0.0\n"
        rectangle = Rectangle((0, 0), 5, 3,
                              rotation=45,
                              bgcolor=3,
                              layer='RECTANGLE')
        self.assertSequenceEqual(normalize_dxf_chunk(dxfstr(rectangle)), normalize_dxf_chunk(expected))

if __name__=='__main__':
    unittest.main()
