#!/usr/bin/env python
#coding:utf-8
# Created: 08.12.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.util import to_string, to_unicode


class TestToString(unittest.TestCase):
    def test_to_string(self):
        layer = to_unicode('ŽĆČĐŠ')
        text = to_unicode('На крај села жута ћирилична кућа')

        self.assertEqual(to_string(layer), r'\U+017d\U+0106\U+010c\U+0110\U+0160')
        self.assertEqual(to_string(text), r'\U+041d\U+0430 \U+043a\U+0440\U+0430\U+0458 \U+0441\U+0435\U+043b\U+0430 \U+0436\U+0443\U+0442\U+0430 \U+045b\U+0438\U+0440\U+0438\U+043b\U+0438\U+0447\U+043d\U+0430 \U+043a\U+0443\U+045b\U+0430')

if __name__=='__main__':
    unittest.main()
