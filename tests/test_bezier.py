#!/usr/bin/env python
#coding:utf-8
# Purpose: test bezier module
# Created: 28.03.2010
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

from dxfwrite.helpers import normalize_dxf_chunk
from dxfwrite.algebra.bezier import CubicBezierCurve
from dxfwrite.curves import Bezier

expected_points = [
    (0.0, 0.0),
    (0.16462499999999999, 0.57737499999999997),
    (0.35700000000000004, 1.1090000000000002),
    (0.57487500000000002, 1.594125),
    (0.81600000000000028, 2.0320000000000005),
    (1.078125, 2.421875),
    (1.3590000000000002, 2.7629999999999999),
    (1.6563750000000002, 3.0546249999999997),
    (1.9680000000000002, 3.2960000000000003),
    (2.2916250000000007, 3.4863750000000007),
    (2.625, 3.625), (2.9658750000000005, 3.711125),
    (3.3120000000000007, 3.7440000000000002),
    (3.6611250000000002, 3.7228750000000002),
    (4.011000000000001, 3.6470000000000002),
    (4.359375, 3.515625),
    (4.7040000000000006, 3.3280000000000003),
    (5.042625000000001, 3.0833749999999993),
    (5.3730000000000002, 2.7809999999999997),
    (5.6928750000000008, 2.4201249999999996),
    (6.0, 2.0)
]

expected_dxf = "  0\nPOLYLINE\n 62\n256\n  8\n0\n 66\n1\n 10\n0.0\n 20\n0.0\n"\
" 30\n0.0\n 70\n8\n  0\nVERTEX\n  8\n0\n 10\n2.0\n 20\n4.0\n 30\n0.0\n  0\n"\
"VERTEX\n  8\n0\n 10\n2.224\n 20\n5.08\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n"\
"2.832\n 20\n5.92\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n3.728\n 20\n6.52\n 30\n"\
"0.0\n  0\nVERTEX\n  8\n0\n 10\n4.816\n 20\n6.88\n 30\n0.0\n  0\nVERTEX\n  8\n"\
"0\n 10\n6.0\n 20\n7.0\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n6.0\n 20\n7.0\n"\
" 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n6.816\n 20\n7.56\n 30\n0.0\n  0\nVERTEX\n"\
"  8\n0\n 10\n7.968\n 20\n7.16\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n9.312\n"\
" 20\n6.28\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n10.704\n 20\n5.4\n 30\n0.0\n"\
"  0\nVERTEX\n  8\n0\n 10\n12.0\n 20\n5.0\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n"\
"12.0\n 20\n5.0\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n13.136\n 20\n5.128\n 30\n"\
"0.0\n  0\nVERTEX\n  8\n0\n 10\n14.128\n 20\n5.544\n 30\n0.0\n  0\nVERTEX\n  8\n"\
"0\n 10\n14.952\n 20\n6.296\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n15.584\n 20\n"\
"7.432\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n16.0\n 20\n9.0\n 30\n0.0\n  0\nSEQEND\n"

class TestAlgebraCubicBezier(unittest.TestCase):
    def test_base_curve(self):
        test_points = [(0, 0), (1, 4), (4, 5), (6, 2)]
        bezier = CubicBezierCurve(test_points)
        results = bezier.approximate(20)
        for expected, result in zip(expected_points, results):
            self.assertAlmostEqual(expected[0], result[0])
            self.assertAlmostEqual(expected[1], result[1])

    def test_init_three_points(self):
        test_points = [(0, 0), (1, 4), (4, 5)]
        self.assertRaises(ValueError, CubicBezierCurve, test_points)

    def test_get_tangent(self):
        bezier = CubicBezierCurve([(0, 0), (1, 4), (4, 5), (6, 2)])
        tangent = bezier.get_tangent(0.5)
        self.assertAlmostEqual(tangent[0], 6.75)
        self.assertAlmostEqual(tangent[1], 2.25)

    def test_get_tangent_error(self):
        bezier = CubicBezierCurve([(0, 0), (1, 4), (4, 5), (6, 2)])
        self.assertRaises(ValueError, bezier.get_tangent, 2.)
        self.assertRaises(ValueError, bezier.get_tangent, -2.)

class TestDXFBezier(unittest.TestCase):
    def test_bezier(self):
        bezier = Bezier(color=256, layer='0', linetype=None)
        bezier.start(point=(2, 4), tangent=(0, 2))
        bezier.append(point=(6, 7), tangent1=(-2, 0), tangent2=(1, 2), segments=5)
        bezier.append(point=(12, 5), tangent1=(-2, 0), segments=5)
        bezier.append(point=(16, 9), tangent1=(-0.5, -3), segments=5)

        #test implementation
        result = bezier.__dxf__()
        self.assertSequenceEqual(normalize_dxf_chunk(expected_dxf), normalize_dxf_chunk(result))

    def test_to_few_points(self):
        bezier = Bezier(color=256, layer='0', linetype=None)
        bezier.start(point=(2, 4), tangent=(0, 2))
        segment_generator = bezier._build_bezier_segments()
        self.assertRaises(ValueError, next, segment_generator)
        self.assertRaises(ValueError, bezier.__dxftags__)

if __name__=='__main__':
    unittest.main()
