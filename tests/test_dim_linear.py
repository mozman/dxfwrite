#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.dimlines
# Created: 16.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest2 as unittest

from dxfwrite.dimlines import LinearDimension
class TestLinearDimAPI(unittest.TestCase):
    def test_init(self):
        dimline = LinearDimension(pos=(5, 5),
                                  measure_points=[(0, 0),(10, 0)],
                                  angle = 0.,
                                  dimstyle='default',
                                  layer="LINEARDIMENSION",
                                  roundval=1)
        dxf = dimline.__dxf__()
        self.assertTrue('LINEARDIMENSION' in dxf)

    def test_set_text(self):
        dimline = LinearDimension(
            (5, 5), [(0, 0), (5, 0), (10, 0), (15, 0), (20, 0)])
        dimline.set_text(1, 'override')
        self.assertEqual(dimline.text_override[1], 'override')
        dxf = dimline.__dxf__()
        self.assertTrue('override' in dxf)
        self.assertRaises(IndexError, dimline.set_text, 5, 'out of range')

    def test_count(self):
        dimline = LinearDimension(
            (5, 5), [(0, 0), (5, 0), (10, 0), (15, 0), (20, 0)])
        self.assertEqual(dimline.point_count, 5)
        self.assertEqual(dimline.section_count, 4)

class TestLinearDimensionImplementation(unittest.TestCase):
    def test_horiz(self):
        expected = u"  0\nLINE\n 62\n7\n  8\nDIMENSIONS\n 10\n-0.3\n" \
                 " 20\n5.0\n 30\n0.0\n 11\n10.3\n 21\n5.0\n 31\n" \
                 "0.0\n  0\nLINE\n 62\n5\n  8\nDIMENSIONS\n 10\n" \
                 "0.0\n 20\n5.0\n 30\n0.0\n 11\n0.0\n 21\n0.3\n" \
                 " 31\n0.0\n  0\nLINE\n 62\n5\n  8\nDIMENSIONS\n" \
                 " 10\n10.0\n 20\n5.0\n 30\n0.0\n 11\n10.0\n 21\n" \
                 "0.3\n 31\n0.0\n  0\nTEXT\n  8\nDIMENSIONS\n 10\n" \
                 "5.0\n 20\n5.45\n 30\n0.0\n 40\n0.5\n  1\n1000\n" \
                 " 50\n0.0\n  7\nISOCPEUR\n 72\n1\n 73\n2\n" \
                 " 11\n5.0\n 21\n5.45\n 31\n0.0\n  0\nINSERT\n" \
                 "  8\nDIMENSIONS\n  2\nDIMTICK_ARCH\n 10\n0.0\n" \
                 " 20\n5.0\n 30\n0.0\n 41\n1.0\n 42\n1.0\n 50\n" \
                 "0.0\n  0\nINSERT\n  8\nDIMENSIONS\n  2\n" \
                 "DIMTICK_ARCH\n 10\n10.0\n 20\n5.0\n 30\n" \
                 "0.0\n 41\n1.0\n 42\n1.0\n 50\n0.0\n"

        dimline = LinearDimension(pos=(5,5),measure_points=[(0,0),(10,0)])
        self.assertEqual(dimline.__dxf__(), expected)

    def test_45deg(self):
        expected = u"  0\nLINE\n 62\n7\n  8\nDIMENSIONS\n 10\n-0.212132034356\n" \
                 " 20\n-0.212132034356\n 30\n0.0\n 11\n5.21213203436\n 21\n" \
                 "5.21213203436\n 31\n0.0\n  0\nLINE\n 62\n5\n  8\n" \
                 "DIMENSIONS\n 10\n5.0\n 20\n5.0\n 30\n0.0\n 11\n" \
                 "9.78786796564\n 21\n0.212132034356\n 31\n0.0\n" \
                 "  0\nTEXT\n  8\nDIMENSIONS\n 10\n2.18180194847\n" \
                 " 20\n2.81819805153\n 30\n0.0\n 40\n0.5\n  1\n" \
                 "707\n 50\n45.0\n  7\nISOCPEUR\n 72\n1\n 73\n" \
                 "2\n 11\n2.18180194847\n 21\n2.81819805153\n" \
                 " 31\n0.0\n  0\nINSERT\n  8\nDIMENSIONS\n" \
                 "  2\nDIMTICK_ARCH\n 10\n-4.4408920985e-16\n" \
                 " 20\n4.4408920985e-16\n 30\n0.0\n 41\n" \
                 "1.0\n 42\n1.0\n 50\n45.0\n  0\nINSERT\n" \
                 "  8\nDIMENSIONS\n  2\nDIMTICK_ARCH\n" \
                 " 10\n5.0\n 20\n5.0\n 30\n0.0\n 41\n1.0\n" \
                 " 42\n1.0\n 50\n45.0\n"

        dimline = LinearDimension(pos=(5,5),measure_points=[(0,0),(10,0)],
                                  angle=45)
        self.assertEqual(dimline.__dxf__(), expected)

if __name__=='__main__':
    unittest.main()