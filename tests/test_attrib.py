#!/usr/bin/env python
#coding:utf-8
# Purpose: test dxfwrite.entities.Attrib()
# Created: 21.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import dxfstr
from dxfwrite.entities import Attrib

class TestAttdef(unittest.TestCase):
    def test_attrib_simple(self):
        attrib = Attrib()
        expected = "  0\nATTRIB\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n" \
                 " 40\n1.0\n  1\nAttrib\n  2\nATTRIB\n 70\n0\n"
        self.assertEqual(dxfstr(attrib), expected)

    def test_attrib_all_attribs(self):
        attrib = Attrib(
        length=99,
        rotation=30,
        xscale=1.5,
        oblique=75,
        style='ARIAL',
        mirror=1,
        halign=1,
        valign=2,
        alignpoint=(5,5)
        )
        expected = "  0\nATTRIB\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n" \
                 " 40\n1.0\n  1\nAttrib\n  2\nATTRIB\n 70\n0\n" \
                 " 73\n99\n 50\n30.0\n 41\n1.5\n 51\n75.0\n  7\nARIAL\n" \
                 " 71\n1\n 72\n1\n 74\n2\n 11\n5.0\n 21\n5.0\n 31\n0.0\n"
        self.assertEqual(dxfstr(attrib), expected)

if __name__=='__main__':
    unittest.main()
