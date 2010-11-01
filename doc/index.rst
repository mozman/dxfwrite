.. dxfwrite documentation master file, created by
   sphinx-quickstart on Mon Nov 01 20:03:40 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dxfwrite's documentation!
====================================

Create DXF R12 drawings with python.

usage::

   from dxfwrite import DXFEngine as dxf
   drawing = dxf.drawing('test.dxf')
   drawing.add_layer('LINES')
   drawing.add(dxf.line((0, 0), (1, 0), color=7, layer='LINES'))
   drawing.save()

First create a :ref:`Drawing` , than create various
drawing entities by :ref:`DXFEngine` and add them to the drawing with the
:func:`~dxfwrite.drawing.Drawing.add` method. :ref:`Layers <Layer>`,
:ref:`Textstyles <Textstyle>`, :ref:`Views <View>` and
:ref:`Viewports <Viewport>` were created by the :ref:`Drawing` object.

Contents
========

.. toctree::
   :maxdepth: 1

   Drawing

DXF R12 Entities
================

.. toctree::
   :maxdepth: 1

   /entities/arc
   /entities/attdef
   /entities/attrib
   /entities/block
   /entities/circle
   /entities/3dface
   /entities/insert
   /entities/line
   /entities/point
   /entities/polyline
   /entities/shape
   /entities/solid
   /entities/trace
   /entities/text
   /entities/vertex

Composite Entities
==================

.. toctree::
   :maxdepth: 1

   mtext
   linear_dim
   angular_dim
   arc_dim
   radial_dim
   rectangle
   table
   ellipse
   spline
   bezier
   clothoid

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

