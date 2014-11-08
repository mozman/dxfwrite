#!/usr/bin/env python
#coding:utf-8
# Purpose: test dxfwrite.entities.Block()
# Created: 21.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import dxfstr
from dxfwrite.entities import Block, Line

class TestBlock(unittest.TestCase):
    def test_simple_block(self):
        block = Block(name='empty')
        block.add(Line())
        expected = "  0\nBLOCK\n  8\n0\n  2\nempty\n  3\nempty\n 70\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n" \
                 "  0\nLINE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n0.0\n 21\n0.0\n 31\n0.0\n" \
                 "  0\nENDBLK\n"
        self.assertEqual(dxfstr(block), expected)

    def test_empty_block(self):
        block = Block(name='empty')
        self.assertFalse(block.valid())

    def test_block_attribs(self):
        block = Block(name='empty')
        block.add(Line())
        block['xref'] = 'test\\test.dxf'
        expected = "  0\nBLOCK\n  8\n0\n  2\nempty\n  3\nempty\n 70\n0\n" \
                 " 10\n0.0\n 20\n0.0\n 30\n0.0\n  1\ntest\\test.dxf\n" \
                 "  0\nLINE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n0.0\n 21\n0.0\n 31\n0.0\n" \
                 "  0\nENDBLK\n"
        self.assertEqual(dxfstr(block), expected)

if __name__=='__main__':
    unittest.main()
