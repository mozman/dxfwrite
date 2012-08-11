#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: 'flag' example
# Created: 04.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License
import sys
import os
import random

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

def get_random_point():
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    return (x, y)

sample_coords = [get_random_point() for x in range(50)]

flag_symbol = [(0,0), (0, 5), (4, 3), (0, 3)]

filename = 'flags.dxf'
dwg = dxf.drawing(filename)
dwg.add_layer('FLAGS')

# first create a block
flag = dxf.block(name='flag')
# add dxf entities to the block (the flag)
# use basepoint = (x, y) define an other basepoint than (0, 0)
flag.add( dxf.polyline(flag_symbol) )
flag.add( dxf.circle(radius=.4, color=2) )
# define some attributes
flag.add( dxf.attdef(insert=(0.5, -0.5), tag='NAME', height=0.5, color=3) )
flag.add( dxf.attdef(insert=(0.5, -1.0), tag='XPOS', height=0.25, color=4) )
flag.add( dxf.attdef(insert=(0.5, -1.5), tag='YPOS', height=0.25, color=4) )

# add block definition to the drawing
dwg.blocks.add(flag)
number = 1
for point in sample_coords:
    # now insert flag symbols at coordinate 'point'
    # insert2 needs the block definition object as parameter 'blockdef'
    # see http://packages.python.org/dxfwrite/entities/insert2.html
    # fill attribtes by creating a dict(), keystr is the 'tag' name of the
    # attribute
    values = {
        'NAME': "P(%d)" % number,
        'XPOS': "x = %.3f" % point[0],
        'YPOS': "y = %.3f" % point[1]
    }
    randomscale = 0.5 + random.random() * 2.0
    dwg.add(dxf.insert2(blockdef=flag, insert=point,
                        attribs=values,
                        xscale=randomscale,
                        yscale=randomscale,
                        layer='FLAGS', rotation=-15))
    number += 1

dwg.save()
print("drawing '%s' created.\n" % filename)
