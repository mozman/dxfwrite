#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import math
from random import random

import dxfwrite

def empty_dxf(dxf, name):
    """ create an empty drawing """
    # create the drawing
    drawing = dxf.drawing(name)
    # and save it
    drawing.save()

def simple_dxf(dxf, name):
    def dxflist_example(x=0, y=0, w=1, h=1):
        # dxf list can contain any dxf entity, that supports __dxf__()
        rect = dxfwrite.DXFList()
        rect.append(dxf.line(start=(x, y), end=(x+w, y), color=1))
        rect.append(dxf.line(start=(x+w, y), end=(x+w, y+h), color=2))
        rect.append(dxf.line(start=(x+w, y+h), end=(x, y+h), color=3))
        rect.append(dxf.line(start=(x, y+h), end=(x, y), color=4))
        return rect

    # create a new drawing
    drawing = dxf.drawing(name)
    # add a LAYER-tableentry called 'dxfwrite'
    drawing.add_layer('dxfwrite')
    # add a VIEWPORT-tableentry
    drawing.add_viewport(
            '*Active',
            center_point=(10,10),
            height = 30,
        )

    # add LINE-entity
    drawing.add(dxf.line((0,0),( 10,0),
        color=dxfwrite.const.BYLAYER,
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

    # add a TEXT-entity
    drawing.add(dxf.text(text="Manfred"))

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
            text='attrib:{0}'.format(x),
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
    # and save the drawing
    drawing.save()

def mtext_dxf(dxf, name):
    """ shows the MText object """
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
        for part in xrange(parts):
            dwg.add(dxf.mtext(text, insert, rotation=(delta*part),
                                 color=color, valign=dxfwrite.TOP))

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

def rectangle_dxf(dxf, name):
    """ show the Rectangle object """
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

def dimline_dxf(dxf, filename):
    # Dimlines are separated from the core library.
    # Dimension lines will not generated by the DXFEngine.

    from dxfwrite.dimlines import dimstyles, LinearDimension, AngularDimension
    from dxfwrite.dimlines import ArcDimension, RadialDimension

    # create a new drawing: dxfwrite.DXFEngine.drawing(filename)
    dwg = dxf.drawing(filename)

    # add block and layer definition to drawing
    dimstyles.setup(dwg)

    # create a dimension line for following points
    points = [ (1.7,2.5), (0,0), (3.3,6.9), (8,12)]

    # define new dimstyles, for predefined ticks see dimlines.py
    dimstyles.new("dots", tick="DIMTICK_DOT", scale=1., roundval=2, textabove=.5)
    dimstyles.new("arrow", tick="DIMTICK_ARROW", tick2x=True, dimlineext=0.)
    dimstyles.new('dots2', tick="DIMTICK_DOT", tickfactor=.5)

    #add linear dimension lines
    dwg.add(LinearDimension((3,3), points, dimstyle='dots', angle=15.))
    dwg.add(LinearDimension((0,3), points, angle=90.))
    dwg.add(LinearDimension((-2,14), points, dimstyle='arrow', angle=-10))

    # next dimline is added as anonymous block
    dimline = LinearDimension((-2,3), points, dimstyle='dots2', angle=90.)
    dimline.set_text(1, 'CATCH')

    # add dimline as anonymous block
    dwg.add_anonymous_block(dimline, layer='DIMENSIONS')

    # add polyline to drawing
    dwg.add(dxf.polyline(points, color=5))

    # There are three dimstyle presets for angular dimension
    # 'angle.deg' (default), 'angle.rad', 'angle.grad' (gon)
    # for deg and grad default roundval = 0
    # for rad default roundval = 3

    # angular dimension in grad (gon)
    dwg.add(AngularDimension(pos=(18, 5), center=(15, 0), start=(20, 0),
                             end=(20, 5), dimstyle='angle.grad'))

    # angular dimension in degree (default dimstyle), with one fractional digit
    dwg.add(AngularDimension(pos=(18, 10), center=(15, 5), start=(20, 5),
                             end=(20, 10), roundval=1))

    dwg.add(ArcDimension(pos=(23, 5), center=(20, 0), start=(25, 0),
                         end=(25, 5), dimstyle='dots2'))

    # RadialDimension has a special tick
    dimstyles.new("radius", height=0.25, prefix='R=')
    dwg.add(RadialDimension((20, 0), (24, 1.5), dimstyle='radius'))
    dwg.save()

def get_cos_sin_mesh(dxf):
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

def polymesh_dxf(dxf, name):
    dwg = dxf.drawing(name) # create a drawing
    dwg.add_viewport( # add the active viewport
        '*Active',
        center_point=(0,0),
        height = 30,
        direction_point=(30,30,10)
        )

    dwg.add(get_cos_sin_mesh(dxf)) # add dxf objects to drawing
    dwg.save() # save dxf drawing

def get_cube(dxf, basepoint, length):
    def scale( point ):
        return ( (basepoint[0]+point[0]*length),
                 (basepoint[1]+point[1]*length),
                 (basepoint[2]+point[2]*length))
    pface = dxf.polyface()
    # cube corner points
    p1 = scale( (0,0,0) )
    p2 = scale( (0,0,1) )
    p3 = scale( (0,1,0) )
    p4 = scale( (0,1,1) )
    p5 = scale( (1,0,0) )
    p6 = scale( (1,0,1) )
    p7 = scale( (1,1,0) )
    p8 = scale( (1,1,1) )

    # define the 6 cube faces
    # look into -x direction
    # Every add_face adds 4 vertices 6x4 = 24 vertices
    # On dxf output double vertices will be removed.
    pface.add_face([p1, p5, p7, p3], color=1) # base
    pface.add_face([p1, p5, p6, p2], color=2) # left
    pface.add_face([p5, p7, p8, p6], color=3) # front
    pface.add_face([p7, p8, p4, p3], color=4) # right
    pface.add_face([p1, p3, p4, p2], color=5) # back
    pface.add_face([p2, p6, p8, p4], color=6) # top
    return pface

def polyface_dxf(dxf, name):
    dwg = dxf.drawing(name) # create a drawing
    dwg.add_viewport( # add the active viewport
        '*Active',
        center_point=(0,0),
        height = 30,
        direction_point=(30,30,10)
        )

    for x in xrange(10):
        for y in xrange(10):
            dwg.add(get_cube(dxf, (x,y, random()), random()))
    dwg.save() # save dxf drawing

def table_dxf(dxf, name):
    dwg = dxf.drawing(name) # create a drawing
    table = dxf.table(insert=(0,0), nrows=10, ncols=3)
    # create a text cell with the default style
    cell = table.textcell(0, 0, 'Zeile1')
    # create a new style
    style = table.new_cellstyle('cell1', color=7, textheight=0.5)
    # set cell style
    cell.style = style
    # cell spans over 2 rows and 2 cols
    cell.span=(2, 2)
    dwg.add(table)
    dwg.save()

def main():
    empty_dxf(dxfwrite.DXFEngine, "example_empty.dxf")
    simple_dxf(dxfwrite.DXFEngine, "example_simple.dxf")
    mtext_dxf(dxfwrite.DXFEngine, "example_mtext.dxf")
    rectangle_dxf(dxfwrite.DXFEngine, "example_rectangle.dxf")
    dimline_dxf(dxfwrite.DXFEngine, "example_dimlines.dxf")
    polymesh_dxf(dxfwrite.DXFEngine, "example_polymesh.dxf")
    polyface_dxf(dxfwrite.DXFEngine, "example_polyface.dxf")
    table_dxf(dxfwrite.DXFEngine, "example_table.dxf")

if __name__=='__main__':
    main()