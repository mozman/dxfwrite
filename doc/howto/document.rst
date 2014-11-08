Document Management
===================

How to start using dxfwrite?
----------------------------

All DXF entities should be created by the :class:`DXFEngine`
object. To do that you have to import the DXF creation engine::

    from dxfwrite import DXFEngine

How to create a new DXF drawing?
--------------------------------

You can create a new DXF drawing by the :meth:`DXFEngine.drawing` method::

    drawing = DXFEngine.drawing('example.dxf')

How to manage global drawing settings?
--------------------------------------

The HEADER section of the DXF file contains settings of variables
associated with the drawing. (for more informations see :ref:`HEADER`)

set/get header variables::

    #set value
    drawing.header['$ANGBASE'] = 30

    #get value
    version = drawing.header['$ACADVER'].value

    # for 2D/3D points use:
    minx, miny, minz = drawing.header['$EXTMIN'].tuple

How to create layers?
---------------------

Layers are stored in the :attr:`layers` attribute in the
:class:`Drawing` class.

To create new layers just use::

    drawing.new_layer('a new layer')

.. seealso:: :ref:`Layer`

Where are all the constants defined?
------------------------------------

here::

    from dxfwrite import const

    drawing.new_layer('TEST', flags=const.LAYER_FROZEN)

How to create a new Textstyle?
------------------------------

Textstyles are stored in the :attr:`styles` attribute in the
:class:`Drawing` class.

To create a new Textstyle use::

    drawing.new_style('BIGTEXT', height=12, font='arial.ttf')

.. seealso:: :ref:`Textstyle`

How to insert XREFs?
--------------------

AutoCAD will not always display the XREFs, other DXF-Viewers are less
restrictive::

    drawing.add_xref('path/drawing.dxf')

.. seealso:: :meth:`Drawing.add_xref`
