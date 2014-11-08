#!/usr/bin/env python
#coding:utf-8
# Created: 21.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.entities import Block, Attdef
from dxfwrite.sections import Blocks

class TestSectionBlocks(unittest.TestCase):
    def test_find_block(self):
        blocks = Blocks()
        blocks.add(Block(name='TEST'))
        found = blocks.find('TEST')
        self.assertEqual(found['name'], 'TEST')

    def test_not_find_block(self):
        blocks = Blocks()
        blocks.add(Block(name='TEST'))
        self.assertRaises(KeyError, blocks.find, 'TEST1')

    def test_find_attdef(self):
        blocks = Blocks()
        block = Block(name='TEST')
        block.add(Attdef(tag='ATT1', text='TEXT1'))
        blocks.add(block)

        found = blocks.find_attdef(tag='ATT1', blockname='TEST')
        self.assertEqual(found['text'], 'TEXT1')
        self.assertRaises(KeyError, blocks.find_attdef, 'ATT2', 'TEST')
        self.assertRaises(KeyError, blocks.find_attdef, 'ATT1', 'TEST2')

if __name__=='__main__':
    unittest.main()
