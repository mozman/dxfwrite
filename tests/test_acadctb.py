#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.acadctb
# Created: 24.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest2 as unittest
from StringIO import StringIO

from dxfwrite.acadctb import UserStyle, UserStyles

class TestUserStyleAPI(unittest.TestCase):
    def test_init(self):
        style = UserStyle(0, dict(
            description="memo",
            color_policy = 3,
            pysical_style_number = 7,
            virtual_style_number = 8,
            screen = 99,
            linepattern_size = 0.7,
            linetype = 17,
            adaptive_linetype = 'FALSE',
            lineweight = 19,
            end_style = 1,
            join_style = 2,
            fill_style = 3
        ))
        self.assertEqual(style.description, "memo")
        self.assertTrue(style.dithering)
        self.assertTrue(style.grayscale)
        self.assertEqual(style.physical_style_number, 7)
        self.assertEqual(style.virtual_style_number, 8)
        self.assertEqual(style.screen, 99)
        self.assertEqual(style.linepattern_size, 0.7)
        self.assertFalse(style.adaptive_linetype)
        self.assertEqual(style.lineweight, 19)
        self.assertEqual(style.end_style, 1)
        self.assertEqual(style.join_style, 2)
        self.assertEqual(style.fill_style, 3)

    def test_get_set_color(self):
        style = UserStyle(0)
        style.set_color(123, 23, 77)
        self.assertEqual(style.get_color(), (123, 23, 77))

    def test_object_color(self):
        style = UserStyle(0)
        style.set_color(123, 77, 1)
        style.set_object_color()
        self.assertTrue(style.has_object_color())

    def test_dithering(self):
        style = UserStyle(0)
        style.dithering = True
        self.assertTrue(style.dithering)
        style.dithering = False
        self.assertFalse(style.dithering)

    def test_grayscale(self):
        style = UserStyle(0)
        style.grayscale = True
        self.assertTrue(style.grayscale)
        style.grayscale = False
        self.assertFalse(style.grayscale)

    def test_dxf_color_index(self):
        style = UserStyle(0)
        self.assertEqual(style.get_dxf_color_index(), 1)
    def test_set_lineweight(self):
        styles = UserStyles()
        style = styles.get_style(5)
        style.set_lineweight(0.5)
        self.assertEqual(style.lineweight, 13)


class TestUserStyleImplementation(unittest.TestCase):
    def test_write(self):
        expected =' 0{\n'\
                  '  name="Color_1\n'\
                  '  localized_name="Color_1\n'\
                  '  description="\n'\
                  '  color=-1\n'\
                  '  color_policy=1\n'\
                  '  physical_style_number=0\n'\
                  '  virtual_style_number=0\n'\
                  '  screen=100\n'\
                  '  linepattern_size=0.5\n'\
                  '  linetype=31\n'\
                  '  adaptive_linetype=TRUE\n'\
                  '  lineweight=0\n'\
                  '  fill_style=73\n'\
                  '  end_style=4\n'\
                  '  join_style=5\n'\
                  ' }\n'
        style = UserStyle(0)
        fp = StringIO()
        style.write(fp)
        result = fp.getvalue()
        fp.close()
        self.assertEqual(result, expected)


class TestUserStylesAPI(unittest.TestCase):
    def setUp(self):
        self.styles = UserStyles(description='TestCase')

    def test_check_index(self):
        styles = self.styles
        self.assertRaises(IndexError, styles.check_color_index, 0)
        self.assertRaises(IndexError, styles.check_color_index, 256)

    def test_set_style(self):
        style = self.styles.set_style(3, dict(description='TestCase'))
        self.assertEqual(style.description, 'TestCase')

    def test_get_style(self):
        self.styles.set_style(3, dict(description='TestCase'))
        style = self.styles.get_style(3)
        self.assertEqual(style.description, 'TestCase')

    def test_get_color(self):
        style = self.styles.set_style(4, dict(description='TestCase'))
        style.set_color(123, 17, 99)
        self.assertEqual(self.styles.get_color(4), (123, 17, 99))

    def test_get_lineweight(self):
        style = self.styles.set_style(5, dict(description='TestCase'))
        style.set_lineweight(0.70)
        self.assertAlmostEqual(self.styles.get_lineweight(5), 0.70)

    def test_get_lineweight_index(self):
        self.assertEqual(self.styles.get_lineweight_index(0.50), 13)

    def test_get_table_lineweight(self):
        self.assertEqual(self.styles.get_table_lineweight(13), 0.50)

    def test_set_table_lineweight(self):
        self.styles.set_table_lineweight(7, 1.70)
        self.assertAlmostEqual(self.styles.get_table_lineweight(7), 1.70)

class TestUserStylesImplementation(unittest.TestCase):
    def test_write_header(self):
        expected = 'description="\n'\
                   'aci_table_available=TRUE\n'\
                   'scale_factor=1.0\n'\
                   'apply_factor=FALSE\n'\
                   'custom_lineweight_display_units=0\n'
        styles = UserStyles()
        fp = StringIO()
        styles._write_header(fp)
        result = fp.getvalue()
        fp.close()
        self.assertEqual(result, expected)

    def test_write_aci_table(self):
        expected = 'aci_table{\n' + '\n'.join(
                     (' {0}="Color_{1}'.format(index, index+1)
                      for index in xrange(255))) + '\n}\n'
        styles = UserStyles()
        fp = StringIO()
        styles._write_aci_table(fp)
        result = fp.getvalue()
        fp.close()
        self.assertEqual(unicode(result), unicode(expected))
    def test_write_lineweights(self):
        expected = 'custom_lineweight_table{\n'\
                   ' 0=0.00\n 1=0.05\n 2=0.09\n 3=0.10\n 4=0.13\n'\
                   ' 5=0.15\n 6=0.18\n 7=0.20\n 8=0.25\n 9=0.30\n'\
                   ' 10=0.35\n 11=0.40\n 12=0.45\n 13=0.50\n 14=0.53\n'\
                   ' 15=0.60\n 16=0.65\n 17=0.70\n 18=0.80\n 19=0.90\n'\
                   ' 20=1.00\n 21=1.06\n 22=1.20\n 23=1.40\n 24=1.58\n'\
                   ' 25=2.00\n 26=2.11\n}\n'
        styles = UserStyles()
        fp = StringIO()
        styles._write_lineweights(fp)
        result = fp.getvalue()
        fp.close()
        self.assertEqual(unicode(result), unicode(expected))

class TestCtbImport(unittest.TestCase):
    pass

if __name__=='__main__':
    unittest.main()