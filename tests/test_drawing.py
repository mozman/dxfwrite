#!/usr/bin/env python
#coding:utf-8
# Created: 27.04.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import os
import re
import unittest

from dxfwrite import DXFEngine as dxf
from dxfwrite.util import is_string

class TestDrawing(unittest.TestCase):
    def test_drawing(self):
        dwg = dxf.drawing()
        res1 = dwg.__dxf__()
        self.assertTrue(is_string(res1))

    def test_properties(self):
        dwg = dxf.drawing()
        self.assertTrue(dwg.linetypes)
        self.assertTrue(dwg.layers)
        self.assertTrue(dwg.styles)
        self.assertTrue(dwg.views)
        self.assertTrue(dwg.viewports)
        self.assertTrue(dwg.ucs)

    def test_add(self):
        dwg = dxf.drawing()
        self.assertEqual(dwg.add("TEST"), "TEST")

    def test_add_modelspace(self):
        dwg = dxf.drawing()
        txt = dwg.modelspace.add(dxf.text('TEST', paper_space=1))
        self.assertEqual(0, txt['paper_space'])

    def test_add_paperspace(self):
        dwg = dxf.drawing()
        txt = dwg.paperspace.add(dxf.text('TEST', paper_space=0))
        self.assertEqual(1, txt['paper_space'])

    def test_anonymous_blockname(self):
        dwg = dxf.drawing()
        self.assertTrue(re.match("^\*U\d*$", dwg.anonymous_blockname('U')))

    def test_add_anonymous_block(self):
        dwg = dxf.drawing()
        blockname = dwg.add_anonymous_block("TEST")
        self.assertTrue(re.match("^\*U\d*$", blockname))
        block = dwg.blocks.find(blockname)
        entity = block.get_data().pop()
        self.assertEqual(entity, "TEST")

    def test_writing(self):
        filename = 'test.dxf'
        try:
            os.remove(filename)
        except OSError:
            pass

        dwg = dxf.drawing()
        dwg.saveas(filename)
        try:
            os.remove(filename)
        except OSError:
            self.assertTrue(False, "Drawing not saved!")

    def test_add_layer(self):
        dwg = dxf.drawing()
        element = dwg.add_layer('TEST')
        self.assertEqual(element['name'], 'TEST')

    def test_add_style(self):
        dwg = dxf.drawing()
        element = dwg.add_style('TEST')
        self.assertEqual(element['name'], 'TEST')

    def test_add_linetype(self):
        dwg = dxf.drawing()
        element = dwg.add_linetype('TEST')
        self.assertEqual(element['name'], 'TEST')

    def test_add_view(self):
        dwg = dxf.drawing()
        element = dwg.add_view('TEST')
        self.assertEqual(element['name'], 'TEST')

    def test_add_viewport(self):
        dwg = dxf.drawing()
        element = dwg.add_vport('TEST')
        self.assertEqual(element['name'], 'TEST')

    def test_add_ucs(self):
        dwg = dxf.drawing()
        element = dwg.add_ucs('TEST')
        self.assertEqual(element['name'], 'TEST')


if __name__=='__main__':
    unittest.main()
