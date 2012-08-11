#!/usr/bin/env python
#coding:utf-8
# Purpose: test base module
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import unittest

from dxfwrite.base import *
from dxfwrite.base import _DXFType
from dxfwrite.util import is_string, to_unicode

class TestAtom(unittest.TestCase):
    def test_atom_cast(self):
        atom = DXFAtom(1.0, 365) # string
        self.assertTrue(is_string(atom._value))
        atom = DXFString('', 1) # empty string
        self.assertEqual(atom._value, '')
        atom = DXFAtom('1.0', 210) # float
        self.assertTrue(isinstance(atom._value, float))
        atom = DXFAtom('7', 295) # bool
        self.assertEqual(atom._value, 1)
        atom = DXFAtom(1.77, 371) # int16
        self.assertTrue(isinstance(atom._value, int))
        self.assertEqual(atom._value, 1)
        atom = DXFAtom('177', 445) # int32
        self.assertTrue(isinstance(atom._value, int))

    def test_equal_DXFAtom(self):
        atom1 = DXFAtom(1.0, 10)
        atom2 = DXFAtom('1.0', 10)
        self.assertEqual(atom1, atom2)
        atom3 = DXFAtom('2.0', 10)
        self.assertNotEqual(atom1, atom3)

    def test_point_coords(self):
        atom = DXFAtom('0', 10) # point, float
        self.assertTrue(isinstance(atom._value, float))
        atom = DXFAtom('0', 20) # point, float
        self.assertTrue(isinstance(atom._value, float))
        atom = DXFAtom('0', 30) # point, float
        self.assertTrue(isinstance(atom._value, float))

    def test_is_3d_point_coord(self):
        atom = DXFAtom('0', 30)
        self.assertTrue(atom.is_3d_point_coord())
        atom = DXFAtom('0', 40)
        self.assertFalse(atom.is_3d_point_coord())

    def test_get_index_shift(self):
        atom = DXFAtom('0', 33)
        self.assertEqual(atom.get_index_shift(), 3)

    def test_get_index_shift_error(self):
        atom = DXFAtom('0', 43)
        self.assertRaises(TypeError, atom.get_index_shift)

    def test_get_axis_index(self):
        atom = DXFAtom('0', 13) # x axis
        self.assertEqual(atom.get_axis_index(), 0)
        atom = DXFAtom('0', 23) # y axis
        self.assertEqual(atom.get_axis_index(), 1)
        atom = DXFAtom('0', 33) # z axis
        self.assertEqual(atom.get_axis_index(), 2)

    def test_get_axis_index_error(self):
        atom = DXFAtom('0', 43)
        self.assertRaises(TypeError, atom.get_axis_index)

    def test_cast_bool(self):
        self.assertFalse(DXFBool('0')._value)
        self.assertTrue(DXFBool('1')._value)
        self.assertFalse(DXFBool(0)._value)
        self.assertTrue(DXFBool(1)._value)

    def test_none_us_chars(self):
        atom = DXFAtom(to_unicode('äöü'), 1) # dxf string
        self.assertEqual(atom.__dxf__(), to_unicode("  1\näöü\n"))

    def test_Atom_to_string_valid(self):
        # numbers < 100 are formatted with leading spaces
        atom = DXFAtom('HEADER', 0)
        self.assertEqual(dxfstr(atom), '  0\nHEADER\n')
        # values > 999 are ok
        atom = DXFAtom ('SECTION', 1000)
        self.assertEqual(dxfstr(atom), '1000\nSECTION\n')
        # float as group_code is ok, converted to int()
        atom = DXFAtom('APP', 1.5)
        self.assertEqual(dxfstr(atom), '  1\nAPP\n')

    def test_invalid_Atom_creation(self):
        # None numeric group code
        self.assertRaises(ValueError, DXFAtom, 'HEADER', 'A')

class TestDXFType(unittest.TestCase):
    def test_check_string(self):
        dxftype = _DXFType()
        self.assertTrue(dxftype.check('string', 1))
        self.assertFalse(dxftype.check(1.0, 1))

    def test_check_bool(self):
        dxftype = _DXFType()
        self.assertTrue(dxftype.check(1, 290))
        self.assertFalse(dxftype.check(2, 290))

    def test_check_float(self):
        dxftype = _DXFType()
        self.assertTrue(dxftype.check(1.0, 10))
        self.assertFalse(dxftype.check('1.0', 10))

    def test_check_int(self):
        dxftype = _DXFType()
        self.assertTrue(dxftype.check(1, 60))
        self.assertFalse(dxftype.check('1', 60))

    def test_check_group_code_error(self):
        dxftype = _DXFType()
        self.assertRaises(ValueError, dxftype.check, '0', 7777)

class TestDXFList(unittest.TestCase):
    def test_empty_DXFList(self):
        atoms = DXFList()
        self.assertEqual(dxfstr(atoms), '')

    def test_DXFList_to_string(self):
        atoms = DXFList()
        atoms.append(DXFAtom('HEADER'))
        atoms.append(DXFAtom('SECTION', 1))
        self.assertEqual(dxfstr(atoms), '  0\nHEADER\n  1\nSECTION\n')

    def test_equal_DXFList(self):
        l  = [DXFAtom(name) for name in ('TEST', 'NAME', 'CODE', 'SOMETHING')]
        dxflist1 = DXFList(l)
        dxflist2 = DXFList(l)

        self.assertEqual(dxflist1, dxflist2)
        dxflist1.append(DXFAtom('ITEM'))
        self.assertNotEqual(dxflist1, dxflist2)

        dxflist3 = DXFList(dxflist1)
        dxflist3[0] = DXFAtom('MODIFY')
        self.assertNotEqual(dxflist1, dxflist3)

    def test_endswith(self):
        dxflist = DXFList()
        self.assertFalse(dxflist.endswith('SEQEND'))
        dxflist.append(DXFAtom('HEADER'))
        self.assertFalse(dxflist.endswith('SEQEND'))
        dxflist.append(DXFAtom('SEQEND'))
        self.assertTrue(dxflist.endswith('SEQEND'))


class TestDXFPoint(unittest.TestCase):
    def test_init(self):
        self.assertEqual(dxfstr(DXFPoint()), ' 10\n0.0\n 20\n0.0\n 30\n0.0\n')
        point = DXFPoint((1., 2., 3.))
        self.assertEqual(dxfstr(point), ' 10\n1.0\n 20\n2.0\n 30\n3.0\n')
        # index shift
        point = DXFPoint((7., 8.), index_shift=3) # 2d point
        self.assertEqual(dxfstr(point), ' 13\n7.0\n 23\n8.0\n')
        # more than 3 or less than 2 coords raises a ValueError
        self.assertRaises(ValueError, DXFPoint, (0., 0., 0., 0.) )
        self.assertRaises(ValueError, DXFPoint, (0., ) )

    def test_index_access(self):
        point = DXFPoint( (7., 8., 9.) )
        self.assertEqual(point[0], 7.)
        self.assertEqual(point[1], 8.)
        self.assertEqual(point[2], 9.)
        self.assertEqual(point['x'], 7.)
        self.assertEqual(point['y'], 8.)
        self.assertEqual(point['z'], 9.)
        self.assertEqual(point['xy'], [7., 8.])
        self.assertEqual(point['yx'], [8., 7.])
        self.assertEqual(point['zyx'], [9., 8., 7.])
        self.assertEqual(point['xxyxx'], [7., 7., 8., 7., 7.])
        self.assertRaises(IndexError, point.__getitem__, 3)
        self.assertRaises(IndexError, point.__getitem__, 'a')
        # 2D-point raises IndexError for axis 'z'
        point.point = ( (DXFFloat(7., 10), DXFFloat(8., 20)) )
        self.assertRaises(IndexError, point.__getitem__, 2)
        self.assertRaises(IndexError, point.__getitem__, 'z')

    def test_swap_xy(self):
        point = DXFPoint( (7., 8.) )
        point2 = DXFPoint(point['yx'])
        self.assertEqual(point2['x'], point['y'])

    def test_max_x(self):
        points = [DXFPoint(coords) for coords in [(1.,2.), (2.,2.), (3.,2.), (4.,2.)]]
        max_x = max( (point['x'] for point in points) ) # by generator
        self.assertEqual(max_x, 4.)

    def test_shift_index(self):
        point = DXFPoint( (1., 2.) )
        self.assertEqual(point.point[0].group_code, 10)
        shifted_point = point.shift_group_code(3)
        self.assertEqual(shifted_point.point[0].group_code, 13)
        self.assertEqual(point['xy'], shifted_point['xy'])

    def test_to_3D_default_zvalue(self):
        point = DXFPoint((1., 2.), 3)
        point.to_3D()
        self.assertEqual(point.point[2].value, 0)

    def test_to_3D_zvalue(self):
        point = DXFPoint((1., 2.), 3)
        point.to_3D(7)
        self.assertEqual(point.point[2].value, 7)

    def test_to_3D_on_3d_point(self):
        point = DXFPoint((1., 2., 3.), 3)
        point.to_3D(7) # only 2D-points will be extended to 3D
        self.assertEqual(point.point[2].value, 3)

    def test_to_3D_group_code(self):
        point = DXFPoint((1., 2.), 3)
        point.to_3D()
        self.assertEqual(point.point[2].group_code, 33)

        point = DXFPoint((1., 2.), 200)
        point.to_3D()
        self.assertEqual(point.point[2].group_code, 230)

    def test_DXFPoint3D(self):
        p = DXFPoint3D( (1., 2.) )
        self.assertEqual(len(p.point), 3)
        self.assertEqual(p.point[2].value, 0.)

    def test_get_value_2D(self):
        p = DXFPoint( (1., 2.) )
        self.assertEqual(p.tuple, (1., 2.))

    def test_get_value_3D(self):
        p = DXFPoint( (1., 2., 3.) )
        self.assertEqual(p.tuple, (1., 2., 3.))


if __name__=='__main__':
    unittest.main()
