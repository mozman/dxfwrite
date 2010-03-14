#!/usr/bin/env python
#coding:utf-8
# Author:  Manfred Moitzi
# Purpose: test dxfwrite.util functions
# Created: 12.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest

from dxfwrite.util import int2hex, hex2int, truecolor
from dxfwrite.util import flatten, iterflatlist
from dxfwrite.base import DXFList, DXFAtom

class TestUtil(unittest.TestCase):
    def test_int2hex(self):
        self.assertEqual(int2hex(255), 'FF')
        self.assertEqual(int2hex(0), '0')

    def test_hex2int(self):
        self.assertEqual(hex2int('FF'), 255)
        self.assertEqual(hex2int('0'), 0)

    def test_int2hex2int(self):
        for i in xrange(1000):
            self.assertEqual(hex2int(int2hex(i)), i)

    def test_truecolor(self):
        self.assertEqual(truecolor( (0,0,0) ), 0)
        self.assertEqual(truecolor( (0,0,255) ), 255)
        self.assertEqual(truecolor( (0,255,0) ), hex2int('0x00ff00'))
        self.assertEqual(truecolor( (255,0,0) ), hex2int('0xff0000'))
        self.assertEqual(truecolor( (255,255,0) ), hex2int('0xffff00'))
        self.assertEqual(truecolor( (255,255,255) ), hex2int('0xffffff'))

    def test_flatten(self):
        l1 = [1,2,3]
        l2 = [3,4,l1]
        l3 = [l2,7]
        self.assertEqual(flatten(l3), [3,4,1,2,3,7])

    def test_dxf_flatten(self):
        dxf = DXFList()
        dxf.append(DXFList( [DXFAtom('HEADER')] ))
        result = flatten(dxf)
        self.assertEqual(result[0].value, 'HEADER')

    def test_iterflatten(self):
        l1 = [1,2,3]
        l2 = [3,4,l1]
        l3 = [l2,7]
        self.assertEqual(list(iterflatlist(l3)), [3,4,1,2,3,7])

if __name__=='__main__':
    unittest.main()