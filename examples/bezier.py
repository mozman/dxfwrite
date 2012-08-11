#!/usr/bin/env python
#coding:utf-8
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

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
from dxfwrite.vector2d import vadd

def draw_control_point(point, tangent1, tangent2=(0, 0)):
    tp1 = vadd(point, tangent1)
    tp2 = vadd(point, tangent2)
    dwg.add(dxf.circle(0.05, center=point, color=1))
    dwg.add(dxf.line(point, tp1, color=2))
    dwg.add(dxf.line(point, tp2, color=2))

name = 'bezier.dxf'
dwg = dxf.drawing(name)
bezier = dxf.bezier(color=4)
dwg.add(bezier)

# define start point
bezier.start((2, 4), tangent=(0, 2))
draw_control_point((2, 4), (0, 2))

# append first point
bezier.append((6, 7), tangent1=(-2, 0), tangent2=(1, 2))
draw_control_point((6, 7), (-2, 0), (1, 2))

# tangent2 = -tangent1 = (+2, 0)
bezier.append((12, 5), tangent1=(-2, 0))
draw_control_point((12, 5), (-2, 0), (2, 0))

# for last point tangent2 is meaningless
bezier.append((16, 9), tangent1=(-0.5, -3))
draw_control_point((16, 9), (-0.5, -3))
dwg.save()
print("drawing '%s' created.\n" % name)
