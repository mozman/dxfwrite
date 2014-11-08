#!/usr/bin/env python
#coding:utf-8
# Created: 21.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import dxfstr
from dxfwrite.entities import Insert, Attrib

class TestInsert(unittest.TestCase):
    def test_insert_simple(self):
        insert = Insert(blockname='empty')
        expected = "  0\nINSERT\n  8\n0\n  2\nempty\n 10\n0.0\n 20\n0.0\n 30\n0.0\n"
        self.assertEqual(dxfstr(insert), expected)

    def test_insert_all_attribs(self):
        insert = Insert(
            attribs_follow = 1,
            blockname='empty',
            xscale=1.0,
            yscale=2.0,
            zscale=3.0,
            rotation=30.0,
            columns=2,
            rows=7,
            colspacing=1.7,
            rowspacing=2.9
        )
        expected = "  0\nINSERT\n  8\n0\n 66\n1\n  2\nempty\n" \
                 " 10\n0.0\n 20\n0.0\n 30\n0.0\n" \
                 " 41\n1.0\n 42\n2.0\n 43\n3.0\n 50\n30.0\n" \
                 " 70\n2\n 71\n7\n 44\n1.7\n 45\n2.9\n"
        self.assertEqual(dxfstr(insert), expected)

    def test_add_attrib_absolute(self):
        block_ref = Insert(blockname='TestAttrib',
                                    insert=(5, 5),
                                    rotation=30)
        attrib = Attrib(
            insert=(1, 1),
            rotation=15,
            tag='TEST',
            text='attrib',
        )
        block_ref.add(attrib, relative=False)
        inserted_attrib = block_ref.data[0]
        self.assertEqual(inserted_attrib['rotation'], 15.)
        self.assertEqual(inserted_attrib['insert']['xy'], [1., 1.])

    def test_add_attrib_relative(self):
        # insert blockref with 45 degree rotation
        block_ref = Insert(blockname='TestAttrib',
                                    insert=(0, 0),
                                    rotation=45)
        attrib = Attrib(
            insert=(1, 1),
            rotation=45, # 45 degree relative to original block definition
            tag='TEST',
            text='attrib',
        )
        block_ref.add(attrib, relative=True) # result rotation = 45 + 45 = 90
        inserted_attrib = block_ref.data[0]
        self.assertEqual(inserted_attrib['rotation'], 90.)
        self.assertAlmostEqual(inserted_attrib['insert']['x'], 0, places=3)
        self.assertAlmostEqual(inserted_attrib['insert']['y'], 1.4142, places=3) # y = sqrt(2)


if __name__=='__main__':
    unittest.main()
