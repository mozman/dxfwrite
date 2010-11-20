#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
import os

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

name = 'spline.dxf'
dwg = dxf.drawing(name)
spline_points = [(0.0, 0.0), (1., 2.), (3., 1.), (5., 3.)]
dwg.add(dxf.spline(spline_points, color=7))
for point in spline_points:
    dwg.add(dxf.circle(radius=0.1, center=point, color=1))
dwg.save()
print("drawing '%s' created.\n" % name)
