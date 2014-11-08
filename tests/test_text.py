#!/usr/bin/env python
#coding:utf-8
# Created: 21.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import dxfstr
from dxfwrite.entities import Text

class TestText(unittest.TestCase):
    def test_circle_no_attributes(self):
        text = Text(text='Manfred')
        expected = "  0\nTEXT\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 40\n1.0\n  1\nManfred\n"
        self.assertEqual(dxfstr(text), expected)

    def test_text_with_attribs(self):
        text = Text(
            text='Manfred',
            height=0.7,
            rotation=30,
            xscale=2,
            oblique=75,
            style='ARIAL',
            mirror=0,
            halign=0,
            valign=0,
            alignpoint = (0,0)
        )
        expected = "  0\nTEXT\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 40\n0.7\n  1\nManfred\n" \
                 " 50\n30.0\n 41\n2.0\n 51\n75.0\n  7\nARIAL\n 71\n0\n 72\n0\n 73\n0\n" \
                 " 11\n0.0\n 21\n0.0\n 31\n0.0\n"
        self.assertEqual(dxfstr(text), expected)

if __name__=='__main__':
    unittest.main()
