#!/usr/bin/env python
#coding:utf-8
# Created: 27.03.2010
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

from dxfwrite.helpers import normalize_dxf_chunk
from dxfwrite.base import dxfstr, DXFInt
from dxfwrite.const import POLYLINE_CLOSED

from dxfwrite.curves import Ellipse

expected = "  0\nPOLYLINE\n  6\nSOLID\n 62\n3\n  8\n0\n 66\n1\n 10\n0.0\n 20\n" \
"0.0\n 30\n0.0\n 70\n8\n  0\nVERTEX\n  8\n0\n 10\n4.33012701892\n 20\n2.5\n 30\n" \
"0.0\n  0\nVERTEX\n  8\n0\n 10\n4.16225056329\n 20\n2.74261781728\n 30\n0.0\n  0\n" \
"VERTEX\n  8\n0\n 10\n3.95428935941\n 20\n2.9588227257\n 30\n0.0\n  0\nVERTEX\n" \
"  8\n0\n 10\n3.70824618737\n 20\n3.14653255383\n 30\n0.0\n  0\nVERTEX\n  8\n0\n" \
" 10\n3.42649057741\n 20\n3.30393955338\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"3.11173599008\n 20\n3.42952780893\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"2.76701368411\n 20\n3.5220878369\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"2.39564352377\n 20\n3.58072823363\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"2.0012020067\n 20\n3.60488426005\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"1.58748782034\n 20\n3.59432328042\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"1.15848525845\n 20\n3.54914700274\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"0.718325850239\n 20\n3.46979049926\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"0.271248571411\n 20\n3.35701801649\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"-0.17844097944\n 20\n3.21191561509\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"-0.626412046113\n 20\n3.0358807105\n 30\n0.0\n  0\nVERTEX\n  8\n0\n 10\n" \
"-1.06835042235\n 20\n2.83060861509\n 30\n0.0\n  0\nSEQEND\n"

class TestEllipse(unittest.TestCase):
    def test_api(self):
        ellipse = Ellipse(center=(0., 0.), rx=5.0, ry=3.0,
                          startangle=0., endangle=360., rotation=30.,
                          segments=100, color=3, layer='0', linetype='SOLID')
        self.assertNotEqual(ellipse, None)

    def test_implementation(self):
        ellipse = Ellipse(center=(0., 0.), rx=5.0, ry=3.0,
                          startangle=0., endangle=90., rotation=30.,
                          segments=16, color=3, layer='0', linetype='SOLID')
        result = dxfstr(ellipse)
        self.assertSequenceEqual(normalize_dxf_chunk(result), normalize_dxf_chunk(expected))
        
    def test_closed_ellipse(self):
        ellipse = Ellipse(center=(0., 0.), rx=5.0, ry=3.0,
                          startangle=0., endangle=360., rotation=30.,
                          segments=16, color=3, layer='0', linetype='SOLID')
        flags = 0
        for tag in ( t for t in ellipse.__dxftags__() if isinstance(t, DXFInt) ):
            if tag.group_code == 70:
                flags = tag.value
                break
                
        self.assertTrue(flags & POLYLINE_CLOSED)

if __name__=='__main__':
    unittest.main()
