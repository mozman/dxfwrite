#!/usr/bin/env python
#coding:utf-8
# Created: 11.12.11
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.mixins import SubscriptAttributes

class MyClass(SubscriptAttributes):
    def __init__(self):
        self.test1 = 0
        self.test2 = "test"

class TestSubscriptAttributes(unittest.TestCase):
    def test_get_existing_attribute(self):
        obj = MyClass()
        self.assertEqual(obj['test1'], obj.test1)

    def test_get_not_existing_attribute(self):
        obj = MyClass()
        with self.assertRaises(KeyError):
            obj['does not exist']

    def test_set_existing_attribute(self):
        obj = MyClass()
        obj['test1'] = "changed"
        self.assertEqual(obj['test1'], "changed")

    def test_set_not_existing_attribute(self):
        obj = MyClass()
        with self.assertRaises(KeyError):
            obj['does not exist'] = 'can only modify existing attributes'

    def test_in_operator(self):
        obj = MyClass()
        self.assertTrue('test1' in obj)

    def test_not_in_operator(self):
        obj = MyClass()
        self.assertTrue('xyz' not in obj)

if __name__ == '__main__':
    unittest.main()
