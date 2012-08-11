#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: examples for dxfwrite usage
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

import sys
import os

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

name = "empty.dxf"
# create the drawing
drawing = dxf.drawing(name)
# and save it
drawing.save()
print("drawing '%s' created.\n" % name)
