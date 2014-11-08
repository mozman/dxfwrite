#!/usr/bin/env python
#coding:utf-8
# Created: 10.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.tableentries import Layer
from dxfwrite import dxfstr, DXFEngine, const


class TestLayerTableEntry(unittest.TestCase):
    expected = "  0\nLAYER\n  2\nStandard\n 70\n0\n 62\n1\n  6\nCONTINUOUS\n"
    def test_create_table_entry(self):
        layer = Layer('Standard', linetype='CONTINUOUS')
        self.assertEqual(dxfstr(layer), self.expected)

    def test_layer_by_factory(self):
        layer = DXFEngine.layer('Standard', linetype='CONTINUOUS')
        self.assertEqual(dxfstr(layer), self.expected)

    def test_layer_off_on(self):
        layer = Layer('Standard', flags=0, color=-7)
        layer.on()
        self.assertEqual(layer['color'], 7)

    def test_layer_on_on(self):
        layer = Layer('Standard', flags=0, color=7)
        layer.on()
        self.assertEqual(layer['color'], 7)

    def test_layer_on_off(self):
        layer = Layer('Standard', flags=0, color=7)
        layer.off()
        self.assertEqual(layer['color'], -7)

    def test_layer_off_off(self):
        layer = Layer('Standard', flags=0, color=-7)
        layer.off()
        self.assertEqual(layer['color'], -7)

    def test_layer_lock(self):
        layer = Layer('Standard', flags=0)
        layer.lock()
        self.assertEqual(layer['flags'], const.STD_FLAGS_LAYER_LOCKED)

    def test_layer_unlock(self):
        layer = Layer('Standard', flags=const.STD_FLAGS_LAYER_LOCKED)
        layer.unlock()
        self.assertEqual(layer['flags'], 0)

    def test_layer_freeze(self):
        layer = Layer('Standard', flags=0)
        layer.freeze()
        self.assertEqual(layer['flags'], const.STD_FLAGS_LAYER_FROZEN)

    def test_layer_thaw(self):
        layer = Layer('Standard', flags=const.STD_FLAGS_LAYER_FROZEN)
        layer.thaw()
        self.assertEqual(layer['flags'], 0)

if __name__=='__main__':
    unittest.main()
