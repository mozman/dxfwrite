#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

import sys
import os

from random import random

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

name="rectangle.dxf"
drawing = dxf.drawing(name)

for x in range(10):
    for y in range(10):
        color = 255 * random()
        bgcolor = 255 * random()
        rand = random()
        # rectangle with only backgound filling
        drawing.add(dxf.rectangle((x*3, y*3) , 1.5*rand, .7*rand,
                                  bgcolor=bgcolor))
        angle = 90 * random()
        # rectangle with only border lines
        drawing.add(dxf.rectangle((40+(x*3), y*3) , 1.5*rand, .7*rand,
                                  color=color, rotation=angle))
drawing.save()
print("drawing '%s' created.\n" % name)


