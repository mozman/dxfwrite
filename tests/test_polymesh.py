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

from dxfwrite.entities import Polymesh
from dxfwrite import dxfstr, const

class TestPolymesh(unittest.TestCase):
    def setUp(self):
        self.addTypeEqualityFunc(str, self.assertMultiLineEqual)

    def test_polymesh(self):
        mesh = Polymesh(2, 2)
        mesh.set_vertex(0, 0, (1, 1, 0))
        vt1 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n1.0\n 30\n0.0\n 70\n64\n"
        mesh.set_vertex(0, 1, (2, 1, 0))
        vt2 = "  0\nVERTEX\n  8\n0\n 10\n2.0\n 20\n1.0\n 30\n0.0\n 70\n64\n"
        mesh.set_vertex(1, 0, (1, 2, 0))
        vt3 = "  0\nVERTEX\n  8\n0\n 10\n1.0\n 20\n2.0\n 30\n0.0\n 70\n64\n"
        mesh.set_vertex(1, 1, (2, 2, 0))
        vt4 = "  0\nVERTEX\n  8\n0\n 10\n2.0\n 20\n2.0\n 30\n0.0\n 70\n64\n"

        expected = "  0\nPOLYLINE\n  8\n0\n 66\n1\n" \
                 " 70\n16\n 71\n2\n 72\n2\n" + vt1 + vt2 + vt3 + vt4 + "  0\nSEQEND\n"
        self.assertEqual(dxfstr(mesh), expected)

    def test_set_mclosed(self):
        mesh = Polymesh(2, 2)
        mesh.set_mclosed(True)
        self.assertTrue(mesh['flags'] & const.POLYLINE_MESH_CLOSED_M_DIRECTION)

        mesh.set_mclosed(False)
        self.assertFalse(mesh['flags'] & const.POLYLINE_MESH_CLOSED_M_DIRECTION)

    def test_set_nclosed(self):
        mesh = Polymesh(2, 2)
        mesh.set_nclosed(True)
        self.assertTrue(mesh['flags'] & const.POLYLINE_MESH_CLOSED_N_DIRECTION)

        mesh.set_nclosed(False)
        self.assertFalse(mesh['flags'] & const.POLYLINE_MESH_CLOSED_N_DIRECTION)



if __name__=='__main__':
    unittest.main()
