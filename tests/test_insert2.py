#!/usr/bin/env python
#coding:utf-8
# Created: 11.04.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite import DXFEngine as dxf
from dxfwrite.base import dxfstr

class TestInsert2(unittest.TestCase):
    def test_insert2(self):
        block = dxf.block('B1')
        att1 = dxf.attdef('TAG1', (1.0, 0.0), height=0.35)
        att2 = dxf.attdef('TAG2', (1.0, 0.5), height=0.35)
        block.add(att1)
        block.add(att2)
        attribs = {'TAG1': 'TextForTAG1', 'TAG2': 'TextForTAG2'}
        blockref = dxf.insert2(block, insert=(0, 0), attribs=attribs)

        result = dxfstr(blockref)
        self.assertTrue('TAG1' in result)
        self.assertTrue('TAG2' in result)
        self.assertTrue('TextForTAG1' in result)
        self.assertTrue('TextForTAG2' in result)

if __name__=='__main__':
    unittest.main()
