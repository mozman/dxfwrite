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

def four_c(A, length, rotation):
    dwg.add(dxf.clothoid(start=(2, 2), length=length, paramA=A,
                         rotation=rotation, color=1))
    dwg.add(dxf.clothoid(start=(2, 2), mirrorx=True, length=length, paramA=A,
                         rotation=rotation, color=2))
    dwg.add(dxf.clothoid(start=(2, 2),mirrory=True, length=length, paramA=A,
                         rotation=rotation, color=3))
    dwg.add(dxf.clothoid(start=(2, 2),mirrorx=True, mirrory=True, length=length, paramA=A,
                         rotation=rotation,color=4))
name = 'clothoid.dxf'
dwg = dxf.drawing(name)
dwg.add(dxf.line((-20,0), (20, 0), linetype="DASHDOT2"))
dwg.add(dxf.line((0, -20), (0, 20), linetype="DASHDOT"))
for rotation in [0, 30, 45, 60, 75, 90]:
    four_c(10., 25, rotation)
dwg.save()
print("drawing '%s' created.\n" % name)
