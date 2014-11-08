#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

import sys
import os

import math

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

def get_cos_sin_mesh():
    msize = 20
    height = 3.
    # create a new polymesh (m*n), here m=n
    mesh = dxf.polymesh(msize, msize)
    delta = math.pi / msize
    for x in range(msize):
        sinx = math.sin(float(x)*delta)
        for y in range(msize):
            cosy = math.cos(float(y)*delta)
            z = sinx * cosy * height
            # set the m,n vertex to 3d point x,y,z
            mesh.set_vertex(x, y, (x, y, z))
    return mesh

name='polymesh.dxf'
dwg = dxf.drawing(name) # create a drawing

# add the active viewport
dwg.add_vport(
    '*ACTIVE',
    center_point=(0,0),
    height = 30,
    direction_point=(30,30,10)
    )

# add dxf objects to drawing
dwg.add(get_cos_sin_mesh())
dwg.save() # save dxf drawing
print("drawing '%s' created.\n" % name)
