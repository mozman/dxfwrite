#!/usr/bin/env python
#coding:utf-8
# Created: 15.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.dimlines import _DimStyles

class Drawing(object):
    """ mock class """
    class Container(list):
        def add(self, item):
            self.append(item)

    def __init__(self):
        self.blocks = Drawing.Container()

class TestDimStyles(unittest.TestCase):
    def test_setup(self):
        dwg = Drawing()
        styles = _DimStyles()
        styles.setup(dwg)
        self.assertTrue(len(dwg.blocks))

    def test_new(self):
        styles = _DimStyles()
        style = styles.new('TESTSTYLE', layer="TESTLAYER")
        self.assertEqual(style.layer, "TESTLAYER")

    def test_get(self):
        styles = _DimStyles()
        styles.new('TESTSTYLE', layer="TESTLAYER")
        style = styles.get('TESTSTYLE')
        self.assertEqual(style.layer, "TESTLAYER")

        
if __name__=='__main__':
    unittest.main()
