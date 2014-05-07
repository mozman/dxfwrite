#!/usr/bin/env python
#coding:utf-8
# Created: 20.02.2010
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

from dxfwrite.base import dxfstr
from dxfwrite.entities import Line

class TestLine(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(str, self.assertMultiLineEqual)

    def test_line_no_attribs(self):
        line = Line(start=(0,0,0), end=(1,1,1))
        expected = "  0\nLINE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n1.0\n 31\n1.0\n"
        self.assertEqual(dxfstr(line), expected)

    def test_line_2d_points(self):
        line = Line(start=(0,0), end=(1,1))
        expected = "  0\nLINE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n1.0\n 31\n0.0\n"
        self.assertEqual(dxfstr(line), expected)

    def test_line_no_attribs(self):
        line = Line(start=(0,0), end=(1,1))
        # 2d points will be converted to 3d
        expected = "  0\nLINE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n1.0\n 31\n0.0\n"
        self.assertEqual(dxfstr(line), expected)

class TestCommonAttribs(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(str, self.assertMultiLineEqual)

    def test_common_attribs(self):
        line = Line(start=(0,0,0), end=(1,1,1))
        line['linetype'] = 'DASHED'
        line['elevation'] = 1.0
        line['thickness'] = 0.70
        line['color'] = 7
        line['layer'] = 'dxfwrite'
        line['paper_space'] = 1
        line['extrusion_direction'] = (0,0,1)
        expected = "  0\nLINE\n  6\nDASHED\n 38\n1.0\n 39\n0.7\n 62\n7\n  8\n" \
                 "dxfwrite\n 67\n1\n210\n0.0\n220\n0.0\n230\n1.0\n" \
                 " 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n1.0\n 21\n1.0\n 31\n1.0\n"
        self.assertEqual(dxfstr(line), expected)


if __name__=='__main__':
    unittest.main()
