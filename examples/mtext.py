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

def textblock(mtext, x, y, rot, color=3, mirror=0):
    dwg.add(dxf.line((x+50, y), (x+50, y+50),  color=color))
    dwg.add(dxf.line((x+100, y), (x+100, y+50), color=color))
    dwg.add(dxf.line((x+150, y), (x+150, y+50), color=color))

    dwg.add(dxf.line((x+50, y), (x+150, y), color=color))
    dwg.add(dxf.mtext(mtext, (x+50, y), mirror=mirror, rotation=rot))
    dwg.add(dxf.mtext(mtext, (x+100, y), mirror=mirror, rotation=rot,
                      halign=dxfwrite.CENTER))
    dwg.add(dxf.mtext(mtext, (x+150, y), mirror=mirror, rotation=rot,
                      halign=dxfwrite.RIGHT))

    dwg.add(dxf.line((x+50, y+25), (x+150, y+25), color=color))
    dwg.add(dxf.mtext(mtext, (x+50, y+25), mirror=mirror, rotation=rot,
                      valign=dxfwrite.MIDDLE))
    dwg.add(dxf.mtext(mtext, (x+100, y+25), mirror=mirror, rotation=rot,
                      valign=dxfwrite.MIDDLE, halign=dxfwrite.CENTER))
    dwg.add(dxf.mtext(mtext, (x+150, y+25), mirror=mirror, rotation=rot,
                      valign=dxfwrite.MIDDLE, halign=dxfwrite.RIGHT))

    dwg.add(dxf.line((x+50, y+50), (x+150, y+50), color=color))
    dwg.add(dxf.mtext(mtext, (x+50, y+50), mirror=mirror,
                      valign=dxfwrite.BOTTOM, rotation=rot))
    dwg.add(dxf.mtext(mtext, (x+100, y+50), mirror=mirror,
                      valign=dxfwrite.BOTTOM, rotation=rot,
                      halign=dxfwrite.CENTER))
    dwg.add(dxf.mtext(mtext, (x+150, y+50), mirror=mirror,
                      valign=dxfwrite.BOTTOM, rotation=rot,
                      halign=dxfwrite.RIGHT))

def rotate_text(text, insert, parts=16, color=3):
    delta = 360. / parts
    for part in range(parts):
        dwg.add(dxf.mtext(text, insert, rotation=(delta*part),
                             color=color, valign=dxfwrite.TOP))

name = "mtext.dxf"
dwg = dxf.drawing(name)
txt = "Das ist ein mehrzeiliger Text\nZeile 2\nZeile 3\nUnd eine lange lange" \
        " ................ Zeile4"

textblock(txt, 0, 0, 0., color=1)
textblock(txt, 150, 0,  45., color=2)
textblock(txt, 300, 0,  90., color=3)

textblock(txt, 0, 70,  135., color=4)
textblock(txt, 150, 70,  180., color=5)
textblock(txt, 300, 70,  225., color=6)

txt = "MText Zeile 1\nMIRROR_X\nZeile 3"
textblock(txt, 0, 140,  0., color=4, mirror=dxfwrite.MIRROR_X)
textblock(txt, 150, 140,  45., color=5, mirror=dxfwrite.MIRROR_X)
textblock(txt, 300, 140,  90., color=6, mirror=dxfwrite.MIRROR_X)

txt = "MText Zeile 1\nMIRROR_Y\nZeile 3"
textblock(txt, 0, 210,  0., color=4, mirror=dxfwrite.MIRROR_Y)
textblock(txt, 150, 210,  45., color=5, mirror=dxfwrite.MIRROR_Y)
textblock(txt, 300, 210,  90., color=6, mirror=dxfwrite.MIRROR_Y)

textblock("Einzeiler  0 deg", 0, -70, 0., color=1)
textblock("Einzeiler 45 deg", 150, -70,  45., color=2)
textblock("Einzeiler 90 deg", 300, -70,  90., color=3)

txt = "--------------------------------------------------Zeile 1\n" \
      "----------------- MTEXT MTEXT --------------------Zeile 2 zum Rotieren!\n" \
      "--------------------------------------------------Zeile 3\n"
rotate_text(txt, (600, 100), parts=16, color=3)
dwg.save()
print("drawing '%s' created.\n" % name)
