#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test _Entity
# Created: 15.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import unittest

from dxfwrite.entities import _Entity

class MockEntity(_Entity):
    name = 'LINE' # so we can use dxf attributes

class TestEntity(unittest.TestCase):
    def test_init(self):
        e = MockEntity()
        self.assertEqual(e['layer'], '0')

    def test_init_with_kwargs(self):
        e = MockEntity(layer='1')
        self.assertEqual(e['layer'], '1')

    def test_set_get_attribute(self):
        e = MockEntity()
        e['layer'] = '1'
        self.assertEqual(e['layer'], '1')

    def test_get_attribute_error(self):
        e = MockEntity()
        self.assertRaises(KeyError, e.__getitem__, 'mozman')

    def test_set_attribute_error(self):
        e = MockEntity()
        self.assertRaises(KeyError, e.__setitem__, 'mozman', 1)

if __name__=='__main__':
    unittest.main()