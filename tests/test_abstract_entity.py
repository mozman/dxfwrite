#!/usr/bin/env python
#coding:utf-8
# Created: 15.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

try:
    # Python 2.6 and earlier need the unittest2 package
    # try: pip install unittest2
    # or download source from: http://pypi.python.org/pypi/unittest2
    import unittest2 as unittest
except ImportError:
    import unittest


from dxfwrite.entities import _Entity, Line

class MockEntity(_Entity):
    DXF_ENTITY_NAME = Line.DXF_ENTITY_NAME
    DXF_ATTRIBUTES = Line.DXF_ATTRIBUTES

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
        with self.assertRaises(KeyError):
            result = e['mozman']

    def test_set_attribute_error(self):
        e = MockEntity()
        with self.assertRaises(KeyError):
            e['mozman'] = 'test'

if __name__=='__main__':
    unittest.main()
