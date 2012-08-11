#!/usr/bin/env python
#coding:utf-8
# Created: 15.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.engine import DXFEngine

class TestDXFEngine(unittest.TestCase):
    def test_drawing(self):
        self.assertTrue(DXFEngine.drawing())

    def test_layer(self):
        self.assertTrue(DXFEngine.layer(name="TEST"))

    def test_style(self):
        self.assertTrue(DXFEngine.style(name="TEST"))

    def test_linetype(self):
        self.assertTrue(DXFEngine.linetype(name="TEST"))

    def test_view(self):
        self.assertTrue(DXFEngine.view(name="TEST"))

    def test_viewport(self):
        self.assertTrue(DXFEngine.vport(name="TEST"))

    def test_ucs(self):
        self.assertTrue(DXFEngine.ucs(name="TEST"))

    def test_appid(self):
        self.assertTrue(DXFEngine.appid(name="TEST"))

    def test_linepattern(self):
        self.assertTrue(DXFEngine.linepattern(pattern=[1, 1, 2, 1]))

    def test_line(self):
        self.assertTrue(DXFEngine.line(start=(0, 0), end=(1, 1)))

    def test_point(self):
        self.assertTrue(DXFEngine.point(point=(0, 0)))

    def test_solid(self):
        self.assertTrue(DXFEngine.solid(points=[(0, 0), (1, 1), (0, 1)]))

    def test_trace(self):
        self.assertTrue(DXFEngine.trace(points=[(0, 0), (1, 1), (0, 1)]))

    def test_circle(self):
        self.assertTrue(DXFEngine.circle(radius=1, center=(0, 0)))

    def test_arc(self):
        self.assertTrue(DXFEngine.arc(radius=1, center=(0, 0), startangle=10,
                                      endangle=350))
    def test_text(self):
        self.assertTrue(DXFEngine.text(text="TEXT", insert=(0, 0), height=3.))

    def test_shape(self):
        self.assertTrue(DXFEngine.shape(name="TEST", insert=(0, 0)))

    def test_insert(self):
        self.assertTrue(DXFEngine.insert(blockname="TEST", insert=(0, 0)))

    def test_attdef(self):
        self.assertTrue(DXFEngine.attdef(tag="TEST", insert=(0, 0)))

    def test_attrib(self):
        self.assertTrue(DXFEngine.attrib(text="TEXT", insert=(0, 0)))

    def test_face3d(self):
        self.assertTrue(DXFEngine.face3d(points=[(0, 0), (1, 1), (0, 1)]))

    def test_block(self):
        self.assertTrue(DXFEngine.block(name="TEST", basepoint=(0, 0)))

    def test_polyline(self):
        self.assertTrue(DXFEngine.polyline(points=[(0, 0), (1, 1), (0, 1)]))

    def test_polymesh(self):
        self.assertTrue(DXFEngine.polymesh(nrows=10, ncols=10))

    def test_polyface(self):
        self.assertTrue(DXFEngine.polyface(precision=5))

    def test_mtext(self):
        self.assertTrue(DXFEngine.mtext("TEXT", insert=(0,0), linespacing=1.5))

    def test_rectangle(self):
        self.assertTrue(DXFEngine.rectangle(insert=(0,0), width=10, height=10))

    def test_table(self):
        self.assertTrue(DXFEngine.table(insert=(0, 0), nrows=10, ncols=10,
                                        default_grid=True))

    def test_ellipse(self):
        self.assertTrue(DXFEngine.ellipse(center=(0,0), rx=3, ry=1))

    def test_spline(self):
        self.assertTrue(DXFEngine.spline(points=[(0,0), (2,1), (5,3)],
                                         segments=100))

    def test_bezier(self):
        self.assertTrue(DXFEngine.bezier())

    def test_clothoid(self):
        self.assertTrue(DXFEngine.clothoid(start=(0,0), length=30, paramA=2))

    def test_insert2(self):
        block = DXFEngine.block('TEST')
        self.assertTrue(DXFEngine.insert2(block, insert=(0,0), attribs={}))

if __name__=='__main__':
    unittest.main()
