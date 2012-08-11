#!/usr/bin/env python
#coding:utf-8
# Created: 10.02.2010
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

from dxfwrite.tableentries import UCS
from dxfwrite import dxfstr, DXFEngine


class TestUCSTableEntry(unittest.TestCase):
    expected = "  0\nUCS\n  2\nTest\n 70\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n" \
             " 11\n1.0\n 21\n0.0\n 31\n0.0\n 12\n0.0\n 22\n1.0\n 32\n0.0\n"

    def test_create_table_entry(self):
        ucs = UCS('Test')
        self.assertEqual(dxfstr(ucs), self.expected)

    def test_ucs_by_factory(self):
        ucs = DXFEngine.ucs('Test')
        self.assertEqual(dxfstr(ucs), self.expected)

if __name__=='__main__':
    unittest.main()
