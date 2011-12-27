#!/usr/bin/env python
#coding:utf-8
# Purpose: try viewports in paperspace
# Created: 27.12.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

__author__ = "mozman <mozman@gmx.at>"

import os
import sys

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))
from dxfwrite import DXFEngine as dxf
from dxfwrite.const import CENTER

def create_modelspace_content(dwg):
    dwg.add(dxf.rectangle((5,5), 5, 5, color=2))
    dwg.add(dxf.circle(2.5, (10, 5), color=3))
    triangle = dxf.polyline([(10, 7.5), (15, 5), (15, 10)], color=4)
    triangle.close(True)
    dwg.add(triangle)

def create_layout(dwg):
    # define viewports in paper space
    dwg.paperspace.add(
        dxf.viewport(center_point=(2.5, 2.5), width=5, height=5,
            view_center_point=(7.5, 7.5),
            view_height=10))
    # scale is calculated by: height of model space (view_height=10) / height of viewport (height=5)
    dwg.paperspace.add(dxf.text("View of Rectangle Scale=1:2", insert=(0, 5.2), height=0.18, color=1))

    dwg.paperspace.add(
        dxf.viewport(center_point=(8.5, 2.5), width=5, height=5,
            view_center_point=(10, 5),
            view_height=25))
    dwg.paperspace.add(dxf.text("View of Circle Scale=1:5", insert=(6, 5.2),
                                height=0.18, color=1))

    dwg.paperspace.add(
        dxf.viewport(center_point=(14.5, 2.5), width=5, height=5,
            view_center_point=(12.5, 7.5),
            view_height=5))
    dwg.paperspace.add(dxf.text("View of Triangle Scale=1:1", insert=(12, 5.2),
                                height=0.18, color=1))

    dwg.paperspace.add(
        dxf.viewport(center_point=(7.5, 10), width=15, height=7.5,
                     view_center_point=(10, 6.25),
                     view_height=7.5))
    dwg.paperspace.add(dxf.text("Overall View Scale=1:1", insert=(0, 14),
                                height=0.18, color=1))

    dwg.paperspace.add(
        dxf.viewport(center_point=(16, 10), width=0.3, height=0.15,
                     view_center_point=(10, 6.25),
                     view_height=7.5))
    # scale = 7.5/0.15 = 50
    dwg.paperspace.add(dxf.text("Scale=1:50", halign=CENTER, alignpoint=(16, 10.5),
                       height=0.18, color=1))


def main():
    dwg = dxf.drawing('viewports_in_paperspace.dxf')
    # IMPORTANT: DXF R12 supports only 1 paper space aka layout
    create_modelspace_content(dwg)
    create_layout(dwg)
    try:
        dwg.save()
    except IOError:
        print("Can't write: '%s'" % dwg.filename)

if __name__=='__main__':
    main()
