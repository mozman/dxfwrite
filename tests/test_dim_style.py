#!/usr/bin/env python
#coding:utf-8
# Created: 15.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.dimlines import _DimStyle

class TestDimStyle(unittest.TestCase):
    def test_get_value(self):
        style = _DimStyle('test', layer="TESTLAYER")
        self.assertEqual(style.layer, "TESTLAYER")

    def test_set_value_as_attibute(self):
        style = _DimStyle('test', )
        style.layer = "TESTLAYER"
        self.assertEqual(style.layer, "TESTLAYER")

    def test_get_set_value_as_dict(self):
        style = _DimStyle('test', )
        style['layer'] = "TESTLAYER"
        self.assertEqual(style['layer'], "TESTLAYER")

if __name__=='__main__':
    unittest.main()
