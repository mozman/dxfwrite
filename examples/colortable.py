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

def color_name(dxf_index):
    try:
        if dxf_index==7:
            return 'BLACK/WHITE'
        else:
            rgb = colors.get_rgb(dxf_index)
            return "%d: (%d, %d, %d)" % (dxf_index, rgb[0], rgb[1], rgb[2])
    except IndexError:
        return "BYLAYER"

def color_square(x, y, color=None, bgcolor=None):
    if color:
        name = color_name(color)
    if bgcolor:
        name = color_name(bgcolor)
    drawing.add(dxf.rectangle((x, y) , 2, 2, color=color, bgcolor=bgcolor))
    drawing.add(dxf.text(name, (x, y-0.4), height=0.18))

name = "colortable.dxf"
drawing = dxf.drawing(name)

colors = dxfwrite.std.DXFColorIndex()
color = 1
for y in range(16):
    for x in range(16):
        x1 = x * 3
        y1 = y * 3
        color_square(x1, y1, color=color)
        color_square(x1+60, y1, bgcolor=color)
        color += 1

index = 0
for y in range(16):
    for x in range(16):
        x1 = x * 3
        y1 = 60 + y * 3
        color1 = colors.get_dxf_color_index((x*16, y*16, 0))
        color2 = colors.get_dxf_color_index((x*16, 0, y*16))
        color3 = colors.get_dxf_color_index((0, x*16, y*16))
        color_square(x1, y1, bgcolor=color1)
        color_square(x1+60, y1, bgcolor=color2)
        color_square(x1+120, y1, bgcolor=color3)
drawing.save()
print("drawing '%s' created.\n" % name)
