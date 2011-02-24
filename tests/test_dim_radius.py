#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.dimlines
# Created: 21.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from __future__ import absolute_import
from dxfwrite.helpers import normalize_dxf_chunk

import sys
if sys.version_info[:2]> (2, 6):
    import unittest
else: # python 2.6 and prior needs the unittest2 package
    import unittest2 as unittest

from dxfwrite.dimlines import RadialDimension

class TestRadialDimAPI(unittest.TestCase):
    def test_init(self):
        dimline = RadialDimension(
            center=(0, 0),
            target=(3, 3),
            length=1.,
            dimstyle='default',
            layer="RADIALDIMENSION",
            roundval=1)
        dxf = dimline.__dxf__()
        self.assertTrue("RADIALDIMENSION" in dxf)

class TestRadialDimImplementation(unittest.TestCase):
    def test_R3(self):
        expected = "  0\nLINE\n 62\n7\n  8\nDIMENSIONS\n 10\n2.29289321881\n"\
                 " 20\n2.29289321881\n 30\n0.0\n 11\n3.0\n 21\n3.0\n 31\n0.0\n"\
                 "  0\nTEXT\n 62\n7\n  8\nDIMENSIONS\n 10\n2.15147186258\n 20\n"\
                 "2.15147186258\n 30\n0.0\n 40\n0.5\n  1\n424\n 50\n45.0\n  7\n"\
                 "ISOCPEUR\n 72\n2\n 73\n2\n 11\n2.15147186258\n 21\n"\
                 "2.15147186258\n 31\n0.0\n  0\nINSERT\n  8\nDIMENSIONS\n  2\n"\
                 "DIMTICK_RADIUS\n 10\n3.0\n 20\n3.0\n 30\n0.0\n 41\n1.0\n 42\n"\
                 "1.0\n 50\n225.0\n"
        dimline = RadialDimension(center=(0, 0), target=(3, 3), length=1.)
        self.assertSequenceEqual(normalize_dxf_chunk(dimline.__dxf__()), normalize_dxf_chunk(expected))

if __name__=='__main__':
    unittest.main()