#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: xref example
# Created: 27.02.2011
# Copyright (C) , Manfred Moitzi
# License: GPLv3

import sys
import os

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

def create_xref(xrefname):
    dwg = dxf.drawing(xrefname)
    for x in range(6):
        dwg.add(dxf.rectangle((x, 0), 1., 1., color=1+x))
    dwg.add(dxf.text('I AM THE XREF', (0.25, 0.25), height=0.5, color=6))
    dwg.save()

def get_host_dwg(drawingname):
    dwg = dxf.drawing(drawingname)
    dwg.add(dxf.text('I AM THE HOST DRAWING', (-0.5, 1.5), 0.5, color=2))
    dwg.add(dxf.rectangle((-1,-1), 10, 3, color=2))
    return dwg

def use_xref_manual(drawingname, xrefname):
    dwg = get_host_dwg(drawingname)
    dwg.add_layer('XREF')
    # AutoCAD 2010 can not resolve XREFS in DXF R12 Format :-(,
    # or with 'dxfwrite' created drawings are malformed XREFS?

    # define xref
    # you have control over flags
    flag = dxfwrite.const.BLK_XREF
    xref = dxf.block(name='xref', flags=flag ,xref=xrefname)
    dwg.blocks.add(xref)

    # using xref
    # you have control over layer
    dwg.add(dxf.insert('xref', layer='XREF'))
    dwg.save()

def use_xref_shortcut(drawingname, xrefname):
    dwg = get_host_dwg(drawingname)
    # AutoCAD 2010 can not resolve XREFS in DXF R12 Format :-(,
    # or with 'dxfwrite' created drawings are malformed XREFS?

    # no control over flags, layer, linetype, ...
    dwg.add_xref(xrefname)
    dwg.save()

xrefname = 'xref_drawing.dxf'
create_xref(xrefname)
use_xref_manual('xref_dxf_usage_1.dxf', xrefname)
use_xref_shortcut('xref_dxf_usage_2.dxf', xrefname)
# AutoCAD accept .dwg files as XREF (but you have to reload references manually)
use_xref_manual('xref_dwg_usage.dxf', 'xref_drawing.dwg')