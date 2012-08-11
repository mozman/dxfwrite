#!/usr/bin/env python
#coding:utf-8
# Created: 22.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.entities import Vertex
from dxfwrite import dxfstr

class TestVertex(unittest.TestCase):
    def test_simple_vertex(self):
        vertex = Vertex()
        expected = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n"
        self.assertEqual(dxfstr(vertex), expected)

    def test_full_vertex(self):
        vertex = Vertex(
            startwidth=0.1,
            endwidth=0.2,
            bulge=0.3,
            flags=0,
            curve_fit_tangent_direction=30.0
        )
        expected = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n" \
                 " 40\n0.1\n 41\n0.2\n 42\n0.3\n 70\n0\n 50\n30.0\n"
        self.assertEqual(dxfstr(vertex), expected)

    def test_face(self):
        face = Vertex(flags=192)
        face[0] = 1
        face[1] = 2
        face[2] = 3
        face[3] = 4
        expected = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n" \
                 " 70\n192\n 71\n1\n 72\n2\n 73\n3\n 74\n4\n"
        self.assertEqual(dxfstr(face), expected)

if __name__=='__main__':
    unittest.main()
