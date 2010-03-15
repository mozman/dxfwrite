#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import math
import dxfwrite

def empty_dxf(engine, name):
    drawing = engine.drawing(name)
    drawing.save()

def simple_dxf(engine, name):
    def add_all_colors(maxcolor):
        for color in xrange(maxcolor):
            drawing.add(engine.line((50, color), (55, color), color=color))
            drawing.add(engine.text("color index: {0}".format(color), (56, color), .35))

    drawing = engine.drawing(name)
    drawing.add_layer('dxfwrite')
    drawing.add_viewport(
            '*Active',
            center_point=(10,10),
            height = 30,
        )
    drawing.add(engine.line(
        start=(0,0),
        end=(10,0),
        color=dxfwrite.const.BYLAYER,
        layer='dxfwrite'
    ))
    add_all_colors(15)
    drawing.add(engine.circle(center=(5,0), radius=5))
    drawing.add(engine.arc(center=(5,0), radius=4, startangle=30, endangle=150))
    drawing.add(engine.point(point=(1,1)))
    drawing.add(engine.solid([(0,0), (1,0), (1,1), (0,1)], color=2))
    drawing.add(engine.solid([(0,1), (1,1), (1,2)], color=3))
    drawing.add(engine.face3d([(5,5), (6,5), (6,6), (5,6)], color=3))
    drawing.add(engine.text(text="Manfred"))
    drawing.add(engine.text(
        text="mozman",
        style="ISOCPEUR",
        height=0.7,
        oblique=15,
        color=5,
        insert=(0,5),
        rotation=30,
    ))
    # create block definition
    block = engine.block(name='Rechteck')
    block.add(rectangle(engine, 0, 0, 1, 1))
    attdef = engine.attdef(
        insert=(.2, .2),
        rotation = 30,
        height=0.25,
        text='test',
        prompt='test eingeben:',
        tag='TEST'
    )
    block.add(attdef)

    drawing.blocks.add(block) # add block to blocks section
    for x in range(1, 10): # now we can insert a block reference
        block_ref = engine.insert(
            blockname='Rechteck',
            insert=(x*2,10),
            rotation=x*6,
            xscale=x,
            yscale=x)

        # add an attribute
        attrib = attdef.new_attrib(
            height=0.18,
            text='attrib:{0}'.format(x),
        )
        # relative insert, respects the block rotation
        block_ref.add(attrib, relative=True)
        drawing.add(block_ref)

    drawing.add(polyline(engine))
    drawing.add(polymesh(engine))
    drawing.add(cube(engine, basepoint=(-5, 0, 3), length=7))
    drawing.add(engine.line((0,-3), (3,-3)))
    drawing.add(engine.text("aligned Text", insert=(0, -3),
                            halign=dxfwrite.ALIGNED, alignpoint=(3, -3)))
    drawing.add(engine.line((0,-6), (3,-6)))
    drawing.add(engine.text("fitted Text", insert=(0, -6),
                            halign=dxfwrite.FIT, alignpoint=(3, -6)))
    drawing.add(engine.line((0,-9), (3,-9)))
    drawing.add(engine.text("baseline_middle Text", insert=(0, -9),
                            halign=dxfwrite.BASELINE_MIDDLE, alignpoint=(3, -9)))
    drawing.save()

def rectangle(engine, x=0, y=0, w=1, h=1):
    # dxf list can contain any dxf entity, that supports __dxf__()
    rect = dxfwrite.DXFList()
    rect.append(engine.line(start=(x, y), end=(x+w, y), color=1))
    rect.append(engine.line(start=(x+w, y), end=(x+w, y+h), color=2))
    rect.append(engine.line(start=(x+w, y+h), end=(x, y+h), color=3))
    rect.append(engine.line(start=(x, y+h), end=(x, y), color=4))
    return rect

def polyline(engine):
    points = [(20,20), (25,25), (25, 30), (20, 35, 10)]
    pline = engine.polyline(color=3)
    for num, point in enumerate(points):
        width = .05
        pline.add_vertex(point, startwidth=width, endwidth=width, bulge=-.2)
    pline.close()
    return pline

def polymesh(engine):
    mesh = engine.polymesh(3, 3)
    mesh.set_vertex(0,0, (40, 10, 1))
    mesh.set_vertex(0,1, (45, 10, 0))
    mesh.set_vertex(0,2, (50, 10, 0))
    mesh.set_vertex(1,0, (40, 15, 3))
    mesh.set_vertex(1,1, (47, 13, 3))
    mesh.set_vertex(1,2, (50, 15, 3))
    mesh.set_vertex(2,0, (40, 20, 0))
    mesh.set_vertex(2,1, (45, 20, 0))
    mesh.set_vertex(2,2, (50, 20, 1))
    return mesh

def polyface(engine):
    def rect(x, y, z, w, h):
        """ create a rectangle of four vertices """
        return [(x, y, z), (x+w, y, z), (x+w, y+h, z), (x, y+h, z)]
    # a polyface consist of arbritary 3- or 4-sided faces
    mesh = engine.polyface()
    # a face is defined by three or four 3d-points.
    mesh.add_face(rect(40, 10, 0, 10, 10))
    mesh.add_face(rect(55, 10, 0, 10, 10))
    mesh.add_face(rect(45, 15, 1, 10, 10))
    return mesh

def cube(engine, basepoint, length):
    def scale( point ):
        return ( (basepoint[0]+point[0]*length),
                 (basepoint[1]+point[1]*length),
                 (basepoint[2]+point[2]*length))
    pface = engine.polyface()
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

def mtext_dxf(engine, name):
    def textblock(mtext, x, y, rot, color=3, mirror=0):
        dwg.add(engine.line((x+50, y), (x+50, y+50),  color=color))
        dwg.add(engine.line((x+100, y), (x+100, y+50), color=color))
        dwg.add(engine.line((x+150, y), (x+150, y+50), color=color))

        dwg.add(engine.line((x+50, y), (x+150, y), color=color))
        dwg.add(engine.mtext(mtext, (x+50, y), mirror=mirror, rotation=rot))
        dwg.add(engine.mtext(mtext, (x+100, y), mirror=mirror, rotation=rot, halign=dxfwrite.CENTER))
        dwg.add(engine.mtext(mtext, (x+150, y), mirror=mirror, rotation=rot, halign=dxfwrite.RIGHT))

        dwg.add(engine.line((x+50, y+25), (x+150, y+25), color=color))
        dwg.add(engine.mtext(mtext, (x+50, y+25), mirror=mirror, rotation=rot, valign=dxfwrite.MIDDLE))
        dwg.add(engine.mtext(mtext, (x+100, y+25), mirror=mirror, rotation=rot, valign=dxfwrite.MIDDLE, halign=dxfwrite.CENTER))
        dwg.add(engine.mtext(mtext, (x+150, y+25), mirror=mirror, rotation=rot, valign=dxfwrite.MIDDLE, halign=dxfwrite.RIGHT))

        dwg.add(engine.line((x+50, y+50), (x+150, y+50), color=color))
        dwg.add(engine.mtext(mtext, (x+50, y+50), mirror=mirror, valign=dxfwrite.BOTTOM, rotation=rot))
        dwg.add(engine.mtext(mtext, (x+100, y+50), mirror=mirror, valign=dxfwrite.BOTTOM, rotation=rot, halign=dxfwrite.CENTER))
        dwg.add(engine.mtext(mtext, (x+150, y+50), mirror=mirror, valign=dxfwrite.BOTTOM, rotation=rot, halign=dxfwrite.RIGHT))

    def rotate_text(text, insert, parts=16, color=3):
        delta = 360. / parts
        for part in xrange(parts):
            dwg.add(engine.mtext(text, insert, rotation=(delta*part),
                                 color=color, valign=dxfwrite.TOP))

    dwg = engine.drawing(name)
    mtext = "Das ist ein mehrzeiliger Text\nZeile 2\nZeile 3\nUnd eine lange lange" \
            " ................ Zeile4"

    textblock(mtext, 0, 0, 0., color=1)
    textblock(mtext, 150, 0,  45., color=2)
    textblock(mtext, 300, 0,  90., color=3)

    textblock(mtext, 0, 70,  135., color=4)
    textblock(mtext, 150, 70,  180., color=5)
    textblock(mtext, 300, 70,  225., color=6)

    mtext = "MText Zeile 1\nMIRROR_X\nZeile 3"
    textblock(mtext, 0, 140,  0., color=4, mirror=dxfwrite.MIRROR_X)
    textblock(mtext, 150, 140,  45., color=5, mirror=dxfwrite.MIRROR_X)
    textblock(mtext, 300, 140,  90., color=6, mirror=dxfwrite.MIRROR_X)

    mtext = "MText Zeile 1\nMIRROR_Y\nZeile 3"
    textblock(mtext, 0, 210,  0., color=4, mirror=dxfwrite.MIRROR_Y)
    textblock(mtext, 150, 210,  45., color=5, mirror=dxfwrite.MIRROR_Y)
    textblock(mtext, 300, 210,  90., color=6, mirror=dxfwrite.MIRROR_Y)

    textblock("Einzeiler  0 deg", 0, -70, 0., color=1)
    textblock("Einzeiler 45 deg", 150, -70,  45., color=2)
    textblock("Einzeiler 90 deg", 300, -70,  90., color=3)

    mtext = "--------------------------------------------------Zeile 1\n" \
            "----------------- MTEXT MTEXT --------------------Zeile 2 zum Rotieren!\n" \
            "--------------------------------------------------Zeile 3\n"
    rotate_text(mtext, (600, 100), parts=16, color=3)
    dwg.save()

def dimline_dxf(engine, filename):
    # Dimlines are separated from the core library.
    # Dimension lines will not generated by the DXFEngine.

    from dxfwrite.dimlines import dimstyles, LinearDimension, AngularDimension
    from dxfwrite.dimlines import ArcDimension, RadialDimension

    # create a new drawing: dxfwrite.DXFEngine.drawing(filename)
    dwg = engine.drawing(filename)

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
    dwg.add(engine.polyline(points, color=5))

    # There are three dimstyle presets for angular dimension
    # 'angle.deg' (default), 'angle.rad', 'angle.grad' (gon)
    # for deg and grad default roundval = 0
    # for rad default roundval = 3

    # angular dimension in grad (gon)
    dwg.add(AngularDimension(dimlinepos=(18, 5), center=(15, 0), start=(20, 0),
                             end=(20, 5), dimstyle='angle.grad'))

    # angular dimension in degree (default dimstyle), with one fractional digit
    dwg.add(AngularDimension(dimlinepos=(18, 10), center=(15, 5), start=(20, 5),
                             end=(20, 10), roundval=1))

    dwg.add(ArcDimension(dimlinepos=(23, 5), center=(20, 0), start=(25, 0),
                         end=(25, 5), dimstyle='dots2'))

    # RadialDimension has a special tick
    dimstyles.new("radius", height=0.25, prefix='R=')
    dwg.add(RadialDimension((20, 0), (24, 1.5), dimstyle='radius'))
    dwg.save()

def get_3d_entities(engine):
    msize = 20
    height = 3.
    # create a new polymesh (m*n), here m=n
    mesh = engine.polymesh(msize, msize)
    delta = math.pi / msize
    for x in range(msize):
        sinx = math.sin(float(x)*delta)
        for y in range(msize):
            cosy = math.cos(float(y)*delta)
            z = sinx * cosy * height
            # set the m,n vertex to 3d point x,y,z
            mesh.set_vertex(x, y, (x, y, z))
    return [mesh]

def models3d_dxf(engine, name):
    dwg = engine.drawing(name) # create a drawing
    dwg.add_viewport( # add the active viewport
        '*Active',
        center_point=(0,0),
        height = 30,
        direction_point=(30,30,10)
        )

    for dxf_obj in get_3d_entities(engine):
        dwg.add(dxf_obj) # add dxf objects to drawing
    dwg.save() # save dxf drawing

def main():
    empty_dxf(dxfwrite.DXFEngine, "empty.dxf")
    simple_dxf(dxfwrite.DXFEngine, "simple.dxf")
    mtext_dxf(dxfwrite.DXFEngine, "mtext.dxf")
    dimline_dxf(dxfwrite.DXFEngine, "dimlines.dxf")
    models3d_dxf(dxfwrite.DXFEngine, "models3d.dxf")

if __name__=='__main__':
    main()