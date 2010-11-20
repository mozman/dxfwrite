#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: 'flag' example
# Created: 04.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3
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
# add block definition to the drawing
dwg.blocks.add(flag)
for point in sample_coords:
    # now insert flag symbols at coordinate 'point'
    # block are referenced by name, in this case: 'flag'
    # see https://bitbucket.org/mozman/dxfwrite/wiki/Insert
    # additional parameters like xscale, yscale, rotation
    #
    dwg.add(dxf.insert('flag', insert=point, layer='FLAGS', rotation=-15))

dwg.save()
print("drawing '%s' created.\n" % filename)
