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
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

def dxflist_example(x=0, y=0, w=1, h=1):
    # dxf list can contain any dxf entity, that supports __dxf__()
    rect = dxfwrite.DXFList()
    rect.append(dxf.line(start=(x, y), end=(x+w, y), color=1))
    rect.append(dxf.line(start=(x+w, y), end=(x+w, y+h), color=2))
    rect.append(dxf.line(start=(x+w, y+h), end=(x, y+h), color=3))
    rect.append(dxf.line(start=(x, y+h), end=(x, y), color=4))
    return rect

# create a new drawing
name = "simple.dxf"
drawing = dxf.drawing(name)
# add a LAYER-tableentry called 'dxfwrite'
drawing.add_layer('dxfwrite')
# add a VIEWPORT-tableentry
drawing.add_vport(
        '*ACTIVE',
        center_point=(10,10),
        height = 30,
    )

# add LINE-entity
drawing.add(dxf.line((0,0),( 10,0),
    color=dxfwrite.BYLAYER,
    layer='dxfwrite'
))

# add a CIRCLE-entity
drawing.add(dxf.circle(center=(5,0), radius=5))

# add an ARC-entity
drawing.add(dxf.arc(center=(5,0), radius=4, startangle=30, endangle=150))

#add a POINT-entity
drawing.add(dxf.point(point=(1,1)))

# add a SOLID-entity with 4 points
drawing.add(dxf.solid([(0,0), (1,0), (1,1), (0,1)], color=2))

# add a SOLID-entity with 3 points
drawing.add(dxf.solid([(0,1), (1,1), (1,2)], color=3))

# add a 3DFACE-entity
drawing.add(dxf.face3d([(5,5), (6,5), (6,6), (5,6)], color=3))

# add a Trace-entity
drawing.add(dxf.trace([(7,5), (8,5), (8,6), (7,6)], color=4))

# add a TEXT-entity
drawing.add(dxf.text("Manfred"))

# add a TEXT-entity with more properties
drawing.add(dxf.text(
    text="mozman",
    style="ISOCPEUR",
    height=0.7,
    oblique=15,
    color=5,
    insert=(0,5),
    rotation=30,
))

# create BLOCK-entity
block = dxf.block(name='Rechteck')
# add DXF-entities to the block
block.add(dxflist_example(0, 0, 1, 1))
# create an ATTDEF-entity, can be use to crate new ATTRIBS with following
# default values, see attdef.new_attrib() call below
attdef = dxf.attdef(
    insert=(.2, .2),
    rotation = 30,
    height=0.25,
    text='test',
    prompt='test eingeben:', # only important for interactive CAD systems
    tag='TEST'
)
# add attdef to the block definition
block.add(attdef)
# add the block to the BLOCKS section
drawing.blocks.add(block)

# insert the block references
for x in range(1, 10):
    block_ref = dxf.insert(
        blockname='Rechteck',
        insert=(x*2,10),
        rotation=x*6,
        xscale=x,
        yscale=x)

    # create an ATTRIB-entity from an ATTDEF-entity
    attrib = attdef.new_attrib(
        height=0.18,
        text='attrib:%d' % x,
    )

    # add ATTRIB-entity to the block refernce
    # relative insert, respects the block rotation
    block_ref.add(attrib, relative=True)
    # add block reference to drawing
    drawing.add(block_ref)

# example for aligned text
drawing.add(dxf.text("aligned Text", insert=(0, -3),
                        halign=dxfwrite.ALIGNED, alignpoint=(3, -3)))
drawing.add(dxf.line((0,-6), (3,-6)))

# example for fitted text
drawing.add(dxf.text("fitted Text", insert=(0, -6),
                        halign=dxfwrite.FIT, alignpoint=(3, -6)))
drawing.add(dxf.line((0,-9), (3,-9)))

# example for baseline_middle text
drawing.add(dxf.text("baseline_middle Text", insert=(0, -9),
                        halign=dxfwrite.BASELINE_MIDDLE, alignpoint=(3, -9)))

# example for Polyline, flags=0, creates a 2D polyline
# default is a 3D polyline
polyline= dxf.polyline(linetype='DOT', flags=0)
polyline.add_vertices( [(0,20), (3,20), (6,23), (9,23)] )
drawing.add(polyline)

# and save the drawing
drawing.save()
print("drawing '%s' created.\n" % name)


