#!/usr/bin/env python
#coding:utf-8
# Created: 23.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

try:
    # Python 2.6 and earlier need the unittest2 package
    # try: easy_install unittest2
    # or download source from: http://pypi.python.org/pypi/unittest2
    import unittest2 as unittest
except ImportError:
    import unittest

from dxfwrite.entities import Polyface
from dxfwrite import dxfstr

class TestPolyface(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(str, self.assertMultiLineEqual)

    def test_simple_3points_polyface(self):
        pface = Polyface()
        pface.add_face([(0,0), (1,0), (1,1)])
        vt1 = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n192\n"
        vt2 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n0.0\n 30\n0.0\n 70\n192\n"
        vt3 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n 70\n192\n"
        vtface = "  0\nVERTEX\n 62\n0\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n128\n" \
               " 71\n1\n 72\n2\n 73\n3\n"
        expected = "  0\nPOLYLINE\n  8\n0\n 66\n1\n" \
                 " 70\n64\n 71\n3\n 72\n1\n" + vt1 + vt2 + vt3 + vtface + "  0\nSEQEND\n"
        self.assertEqual(dxfstr(pface), expected)

    def test_stable_order(self):
        pface = Polyface()
        pface.add_face([(0,0), (1,1), (1,0)])
        vt1 = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n192\n"
        vt2 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n 70\n192\n"
        vt3 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n0.0\n 30\n0.0\n 70\n192\n"
        vtface = "  0\nVERTEX\n 62\n0\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n128\n" \
               " 71\n1\n 72\n2\n 73\n3\n"
        expected = "  0\nPOLYLINE\n  8\n0\n 66\n1\n" \
                 " 70\n64\n 71\n3\n 72\n1\n" + vt1 + vt2 + vt3 + vtface + "  0\nSEQEND\n"
        self.assertEqual(dxfstr(pface), expected)

    def test_simple_4points_polyface(self):
        pface = Polyface()
        pface.add_face([(0,0), (1,0), (1,1), (0,1)])
        vt1 = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n192\n"
        vt2 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n0.0\n 30\n0.0\n 70\n192\n"
        vt3 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n 70\n192\n"
        vt4 = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n1.0\n 30\n0.0\n 70\n192\n"
        vtface = "  0\nVERTEX\n 62\n0\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n128\n" \
               " 71\n1\n 72\n2\n 73\n3\n 74\n4\n"
        expected = "  0\nPOLYLINE\n  8\n0\n 66\n1\n" \
                 " 70\n64\n 71\n4\n 72\n1\n" + vt1 + vt2 + vt3 + vt4 + vtface + "  0\nSEQEND\n"
        self.assertEqual(dxfstr(pface), expected)

    def test_optimize_simple_4points_polyface(self):
        pface = Polyface()
        pface.add_face([(0,0), (1,0), (1,1), (0,0)]) # 1 == 4 -> use vt1 instead of vt4
        vt1 = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n192\n"
        vt2 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n0.0\n 30\n0.0\n 70\n192\n"
        vt3 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n 70\n192\n"
        vtface = "  0\nVERTEX\n 62\n0\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n128\n" \
               " 71\n1\n 72\n2\n 73\n3\n 74\n1\n"
        expected = "  0\nPOLYLINE\n  8\n0\n 66\n1\n" \
                 " 70\n64\n 71\n3\n 72\n1\n" + vt1 + vt2 + vt3 + vtface + "  0\nSEQEND\n"
        self.assertEqual(dxfstr(pface), expected)

    def test_cube_of_polyfaces(self):
        pface = Polyface()
        # cube corner points
        p1 = pface.add_vertex( (0,0,0) )
        p2 = pface.add_vertex( (0,0,1) )
        p3 = pface.add_vertex( (0,1,0) )
        p4 = pface.add_vertex( (0,1,1) )
        p5 = pface.add_vertex( (1,0,0) )
        p6 = pface.add_vertex( (1,0,1) )
        p7 = pface.add_vertex( (1,1,0) )
        p8 = pface.add_vertex( (1,1,1) )

        # define the 6 cube faces
        # look into -x direction
        pface.add_face_by_indices([p1, p5, p7, p3]) # base
        pface.add_face_by_indices([p1, p5, p6, p2]) # left
        pface.add_face_by_indices([p5, p7, p8, p6]) # front
        pface.add_face_by_indices([p7, p8, p4, p3]) # right
        pface.add_face_by_indices([p1, p3, p4, p2]) # back
        pface.add_face_by_indices([p2, p6, p8, p4]) # top

        vt = "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n192\n" + \
             "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n1.0\n 70\n192\n" + \
             "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n1.0\n 30\n0.0\n 70\n192\n" + \
             "  0\nVERTEX\n  8\n0\n 10\n0.0\n 20\n1.0\n 30\n1.0\n 70\n192\n" + \
             "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n0.0\n 30\n0.0\n 70\n192\n" + \
             "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n0.0\n 30\n1.0\n 70\n192\n" + \
             "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n 70\n192\n" + \
             "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n1.0\n 70\n192\n"

        vtf_prefix = "  0\nVERTEX\n 62\n0\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 70\n128\n"
        vtf =  vtf_prefix + " 71\n1\n 72\n5\n 73\n7\n 74\n3\n" + \
               vtf_prefix + " 71\n1\n 72\n5\n 73\n6\n 74\n2\n" + \
               vtf_prefix + " 71\n5\n 72\n7\n 73\n8\n 74\n6\n" + \
               vtf_prefix + " 71\n7\n 72\n8\n 73\n4\n 74\n3\n" + \
               vtf_prefix + " 71\n1\n 72\n3\n 73\n4\n 74\n2\n" + \
               vtf_prefix + " 71\n2\n 72\n6\n 73\n8\n 74\n4\n"

        expected = "  0\nPOLYLINE\n  8\n0\n 66\n1\n" \
                   " 70\n64\n 71\n8\n 72\n6\n" + vt + vtf + "  0\nSEQEND\n"
        self.assertEqual(dxfstr(pface), expected)

    def test_precision(self):
        pface = Polyface(precision=3)
        pface.add_vertex( (1.0001, 1.0, 1.0) )
        pface.add_vertex( (1.0002, 1.0, 1.0) )
        self.assertEqual(len(pface.vertices), 1)
        pface.add_vertex( (1.001, 1.0, 1.0) )
        self.assertEqual(len(pface.vertices), 2)

if __name__=='__main__':
    unittest.main()
