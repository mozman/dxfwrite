#!/usr/bin/env python
#coding:utf-8
# Created: 12.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.util import int2hex, hex2int
from dxfwrite.util import iterflatlist, set_flag

class TestUtil(unittest.TestCase):
    def test_int2hex(self):
        self.assertEqual(int2hex(255), 'FF')
        self.assertEqual(int2hex(0), '0')

    def test_hex2int(self):
        self.assertEqual(hex2int('FF'), 255)
        self.assertEqual(hex2int('0'), 0)

    def test_int2hex2int(self):
        for i in range(1000):
            self.assertEqual(hex2int(int2hex(i)), i)

    def test_iterflatten(self):
        l1 = [1, 2, 3]
        l2 = [3, 4, l1]
        l3 = [l2, 7]
        self.assertEqual(list(iterflatlist(l3)), [3, 4, 1, 2, 3, 7])

    def test_set_flag_on(self):
        self.assertEqual(set_flag(8, 1 << 2), 12)

    def test_set_flag_off(self):
        self.assertEqual(set_flag(12, 1 << 2, switch_on=False), 8)

if __name__=='__main__':
    unittest.main()
