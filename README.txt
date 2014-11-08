
dxfwrite
========

Abstract
--------

A Python library to create DXF R12 drawings.

a simple example::

    from dxfwrite import DXFEngine as dxf
    drawing = dxf.drawing('test.dxf')
    drawing.add(dxf.line((0, 0), (10, 0), color=7))
    drawing.add_layer('TEXTLAYER', color=2)
    drawing.add(dxf.text('Test', insert=(0, 0.2), layer='TEXTLAYER')
    drawing.save()

supported DXF R12 entities
--------------------------

 * ARC
 * ATTDEF
 * ATTRIB
 * BLOCK
 * CIRCLE
 * 3DFACE
 * INSERT
 * LINE
 * POINT
 * POLYLINE (special Polyface and Polymesh objects are available)
 * SHAPE (not tested)
 * SOLID
 * TRACE
 * TEXT
 * VERTEX (only for internal use, see Polyline, Polyface and Polymesh objects)
 * VIEWPORT

not supported DXF R12 entities
------------------------------

 * DIMENSION

emulated entities from DXF R13 and later
----------------------------------------

 * MTEXT (R13) ... emulated as composite entity MText
 * ELLIPSE (R13) ... approximated by Ellipse
 * SPLINE (R13) ... approximated by Spline
 * LWPOLYLINE (R13) ... use POLYLINE
 * TABLE (R2005) ... emulated as composite entity Table

composite entities
------------------

 * MText -- multi-line text
 * LinearDimension
 * AngularDimension
 * ArcDimension
 * RadialDimension
 * Table -- text and blockrefs containing table like a HTML-table
 * Ellipse -- approximated as POLYLINE
 * Spline -- cubic spline curve through breakpoints **without** additional control
   points, approximated as POLYLINE
 * Bezier -- cubic bezier curve through breakpoints **with** additional control
   points, approximated as POLYLINE
 * Clothoid -- Euler spiral, approximated as POLYLINE

read/write AutoCAD ctb-files
----------------------------

The module ``acadctb`` provides the ability to read and write AutoCAD ctb-files.
With ctb-files you can assign a new color or lineweight to a dxf-color-index for
plotting or printing, but this has to be supported by the used application.

a simple example::

    from dxfwrite import acadctb
    ctb = acadctb.load('test.ctb')
    style1 = ctb.get_style(1) # dxf color index (1 .. 255)
    style1.set_color(23, 177, 68) # set rgb values (0..255)
    style1.set_lineweight(0.7)
    ctb.save('new.ctb')

Installation
------------

with pip::

    pip install dxfwrite

or from source::

    python setup.py install

Documentation
-------------

http://dxfwrite.readthedocs.org
http://packages.python.org/dxfwrite/

The source code repository of dxfwrite can be found at bitbucket.org:

http://bitbucket.org/mozman/dxfwrite

Feedback is greatly appreciated.

mozman <mozman@gmx.at>
