#!/usr/bin/env python
#coding:utf-8
# Created: 21.03.2010
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
from dxfwrite.util import PYTHON3
from dxfwrite.base import dxfstr
from dxfwrite.dimlines import AngularDimension

class TestAngularDimAPI(unittest.TestCase):
    def test_init(self):
        dimline = AngularDimension(
            pos=(5, 5),
            center=(0, 0),
            start=(1, 0),
            end=(1, 1),
            dimstyle='default',
            layer="ANGULARDIMENSION",
            roundval=1)
        dxf = dxfstr(dimline)
        self.assertTrue("ANGULARDIMENSION" in dxf)

class TestAngularDimImplementation(unittest.TestCase):
    def test_45deg(self):
        expected_ = "  0\nARC\n 62\n7\n  8\nDIMENSIONS\n 10\n0.0\n 20\n0.0\n"\
        " 30\n0.0\n 40\n7.07106781187\n 50\n0.0\n 51\n45.0\n  0\nTEXT\n 62\n7\n"\
        "  8\nDIMENSIONS\n 10\n6.94856061401\n 20\n2.8781880453\n 30\n0.0\n"\
        " 40\n0.5\n  1\n%s 50\n-67.5\n  7\nISOCPEUR\n 72\n1\n 73\n2\n"\
        " 11\n6.94856061401\n 21\n2.8781880453\n 31\n0.0\n  0\nINSERT\n  8\n"\
        "DIMENSIONS\n  2\nDIMTICK_RADIUS\n 10\n7.07106781187\n 20\n0.0\n 30\n"\
        "0.0\n 41\n1.0\n 42\n1.0\n 50\n90.0\n  0\nINSERT\n  8\nDIMENSIONS\n"\
        "  2\nDIMTICK_RADIUS\n 10\n5.0\n 20\n5.0\n 30\n0.0\n 41\n1.0\n 42\n"\
        "1.0\n 50\n315.0\n"

        dimline = AngularDimension(pos=(5,5), center=(0, 0), start=(1, 0),
                                   end=(1, 1), )
        if PYTHON3:
            result = dxfstr(dimline)
            expected = expected_ % "45°\n"
        else:
            result = dxfstr(dimline).encode('utf8')
            expected = expected_ % "45\xc2\xb0\n"
        self.assertSequenceEqual(normalize_dxf_chunk(result), normalize_dxf_chunk(expected))

if __name__=='__main__':
    unittest.main()
