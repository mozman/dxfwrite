#!/usr/bin/env python
#coding:utf-8
# Created: 16.03.2010
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

import sys
from dxfwrite.helpers import normalize_dxf_chunk
from dxfwrite.base import dxfstr
from dxfwrite.dimlines import LinearDimension

class TestLinearDimAPI(unittest.TestCase):
    def test_init(self):
        dimline = LinearDimension(pos=(5, 5),
                                  measure_points=[(0, 0),(10, 0)],
                                  angle = 0.,
                                  dimstyle='default',
                                  layer="LINEARDIMENSION",
                                  roundval=1)
        dxf = dxfstr(dimline)
        self.assertTrue('LINEARDIMENSION' in dxf)

    def test_set_text(self):
        dimline = LinearDimension(
            (5, 5), [(0, 0), (5, 0), (10, 0), (15, 0), (20, 0)])
        dimline.set_text(1, 'override')
        self.assertEqual(dimline.text_override[1], 'override')
        dxf = dxfstr(dimline)
        self.assertTrue('override' in dxf)
        self.assertRaises(IndexError, dimline.set_text, 5, 'out of range')

    def test_count(self):
        dimline = LinearDimension(
            (5, 5), [(0, 0), (5, 0), (10, 0), (15, 0), (20, 0)])
        self.assertEqual(dimline.point_count, 5)
        self.assertEqual(dimline.section_count, 4)

# problem with floating-point representation
if sys.version[:3] < '2.6' :
    _float_exp = "e-016"
else:
    _float_exp = "e-16"

class TestLinearDimensionImplementation(unittest.TestCase):
    def test_horiz(self):
        expected = "  0\nLINE\n 62\n7\n  8\nDIMENSIONS\n 10\n-0.3\n" \
                 " 20\n5.0\n 30\n0.0\n 11\n10.3\n 21\n5.0\n 31\n" \
                 "0.0\n  0\nLINE\n 62\n5\n  8\nDIMENSIONS\n 10\n" \
                 "0.0\n 20\n5.0\n 30\n0.0\n 11\n0.0\n 21\n0.3\n" \
                 " 31\n0.0\n  0\nLINE\n 62\n5\n  8\nDIMENSIONS\n" \
                 " 10\n10.0\n 20\n5.0\n 30\n0.0\n 11\n10.0\n 21\n" \
                 "0.3\n 31\n0.0\n  0\nTEXT\n 62\n7\n  8\nDIMENSIONS\n 10\n" \
                 "5.0\n 20\n5.45\n 30\n0.0\n 40\n0.5\n  1\n1000\n" \
                 " 50\n0.0\n  7\nISOCPEUR\n 72\n1\n 73\n2\n" \
                 " 11\n5.0\n 21\n5.45\n 31\n0.0\n  0\nINSERT\n" \
                 "  8\nDIMENSIONS\n  2\nDIMTICK_ARCH\n 10\n0.0\n" \
                 " 20\n5.0\n 30\n0.0\n 41\n1.0\n 42\n1.0\n 50\n" \
                 "0.0\n  0\nINSERT\n  8\nDIMENSIONS\n  2\n" \
                 "DIMTICK_ARCH\n 10\n10.0\n 20\n5.0\n 30\n" \
                 "0.0\n 41\n1.0\n 42\n1.0\n 50\n0.0\n"

        dimline = LinearDimension(pos=(5,5),measure_points=[(0,0),(10,0)])
        self.assertSequenceEqual(normalize_dxf_chunk(dxfstr(dimline)), normalize_dxf_chunk(expected))

    def test_45deg(self):
        expected = "  0\nLINE\n 62\n7\n  8\nDIMENSIONS\n 10\n-0.212132034356\n" \
                 " 20\n-0.212132034356\n 30\n0.0\n 11\n5.21213203436\n 21\n" \
                 "5.21213203436\n 31\n0.0\n  0\nLINE\n 62\n5\n  8\n" \
                 "DIMENSIONS\n 10\n5.0\n 20\n5.0\n 30\n0.0\n 11\n" \
                 "9.78786796564\n 21\n0.212132034356\n 31\n0.0\n" \
                 "  0\nTEXT\n 62\n7\n  8\nDIMENSIONS\n 10\n2.18180194847\n" \
                 " 20\n2.81819805153\n 30\n0.0\n 40\n0.5\n  1\n" \
                 "707\n 50\n45.0\n  7\nISOCPEUR\n 72\n1\n 73\n" \
                 "2\n 11\n2.18180194847\n 21\n2.81819805153\n" \
                 " 31\n0.0\n  0\nINSERT\n  8\nDIMENSIONS\n" \
                 "  2\nDIMTICK_ARCH\n 10\n-4.4408920985%s\n" \
                 " 20\n4.4408920985%s\n 30\n0.0\n 41\n" \
                 "1.0\n 42\n1.0\n 50\n45.0\n  0\nINSERT\n" \
                 "  8\nDIMENSIONS\n  2\nDIMTICK_ARCH\n" \
                 " 10\n5.0\n 20\n5.0\n 30\n0.0\n 41\n1.0\n" \
                 " 42\n1.0\n 50\n45.0\n" % (_float_exp, _float_exp)
        self.maxDiff = None
        dimline = LinearDimension(pos=(5,5),measure_points=[(0,0),(10,0)],
                                  angle=45)
        self.assertSequenceEqual(normalize_dxf_chunk(dxfstr(dimline)), normalize_dxf_chunk(expected))

    def test_dim_points_order(self):
        """ test if point sorting works. """
        points = [ (1.7,2.5), (0,0), (3.3,6.9), (8,12) ]
        dimline = LinearDimension((3,3), points, angle=15.)
        dimline._setup()
        self.assertEqual(dimline.point_order, [1, 0, 2, 3])


if __name__=='__main__':
    unittest.main()
