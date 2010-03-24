#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: test dxfwrite.acadctb
# Created: 24.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest2 as unittest

from dxfwrite.acadctb import Pen, PenStyles

class TestPenAPI(unittest.TestCase):
    def test_init(self):
        pen = Pen(0, dict(description="memo"))
        self.assertEqual(pen.description, "memo")

class TestPenImplementation(unittest.TestCase):
    pass

class TestPenStylesAPI(unittest.TestCase):
    pass

class TestPenStylesImplementation(unittest.TestCase):
    pass

class TestCtbImport(unittest.TestCase):
    pass

if __name__=='__main__':
    unittest.main()