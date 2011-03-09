.. dxfwrite documentation master file, created by
   sphinx-quickstart on Mon Nov 01 20:03:40 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dxfwrite |version| documentation
================================

Welcome! This is the documentation for dxfwrite |version|, last updated |today|.

A Python library to create DXF R12 drawings.

usage::

   from dxfwrite import DXFEngine as dxf

   drawing = dxf.drawing('test.dxf')
   drawing.add_layer('LINES')
   drawing.add(dxf.line((0, 0), (1, 0), color=7, layer='LINES'))
   drawing.save()

First create a :ref:`Drawing` , than create various
drawing entities by :class:`DXFEngine` and add them to the drawing with the
:func:`~dxfwrite.drawing.Drawing.add` method. :ref:`Layers <Layer>`,
:ref:`Textstyles <Textstyle>`, :ref:`Views <View>` and
:ref:`Viewports <Viewport>` were created by the :ref:`Drawing` object.

.. raw:: html

   <a href="http://flattr.com/thing/129228/dxfwrite" target="_blank">
   <img src="http://api.flattr.com/button/flattr-badge-large.png"
   alt="Flattr this" title="Flattr this" border="0" /></a>

Contents
========

.. toctree::
   :maxdepth: 1

   Drawing
   dxfengine

   headervars
   dxftypes
   /entities/layer
   /entities/textstyle


DXF R12 Entities
================

.. toctree::
   :maxdepth: 1

   /entities/arc
   /entities/attdef
   /entities/attrib
   /entities/block
   /entities/circle
   /entities/face3d
   /entities/insert
   /entities/line
   /entities/point
   /entities/polyline
   /entities/polymesh
   /entities/polyface
   /entities/shape
   /entities/solid
   /entities/trace
   /entities/text

Composite Entities
==================

.. toctree::
   :maxdepth: 1

   /entities/mtext
   /entities/insert2
   /entities/linear_dim
   /entities/angular_dim
   /entities/arc_dim
   /entities/radial_dim
   /entities/rect
   /entities/table
   /entities/ellipse
   /entities/spline
   /entities/bezier
   /entities/clothoid

Howtos
======

.. toctree::
   :maxdepth: 1

   /howto/document
   /howto/shapes
   /howto/blocks

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Document License
================

Unless otherwise stated, the content of this document is licensed under
`Creative Commons Attribution-ShareAlike 3.0 License
<http://creativecommons.org/licenses/by-sa/3.0/>`_
