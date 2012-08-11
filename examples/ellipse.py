#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

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

name = 'ellipse.dxf'
dwg = dxf.drawing(name)

for axis in [0.5, 0.75, 1., 1.5,  2., 3.]:
    dwg.add(dxf.ellipse((0,0), 5., axis, segments=200))

dwg.add(dxf.line((-7, 0), (+7, 0), color=1, linetype='DASHDOT'))
dwg.add(dxf.line((0, -5), (0, +5), color=2, linetype='DASHDOT'))

for rotation in [0, 30, 45, 60, 90]:
    dwg.add(dxf.ellipse((20,0), 5., 2., rotation=rotation, segments=100))

for startangle in [0, 30, 45, 60, 90]:
    dwg.add(dxf.ellipse((40,0), 5., 2., startangle=startangle, endangle=startangle+90,
                        rotation=startangle, segments=90))
    dwg.add(dxf.ellipse((40,0), 5., 2., startangle=startangle+180, endangle=startangle+270,
                        rotation=startangle, segments=90))

dwg.save()
print("drawing '%s' created.\n" % name)
