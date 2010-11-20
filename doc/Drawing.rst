.. _Drawing:

Drawing
=======

.. autoclass:: dxfwrite.drawing.Drawing

.. automethod:: dxfwrite.drawing.Drawing.__init__

Methods
-------

.. automethod:: dxfwrite.drawing.Drawing.add

.. automethod:: dxfwrite.drawing.Drawing.save

.. automethod:: dxfwrite.drawing.Drawing.saveas

.. automethod:: dxfwrite.drawing.Drawing.add_layer

.. automethod:: dxfwrite.drawing.Drawing.add_style

.. automethod:: dxfwrite.drawing.Drawing.add_linetype

.. automethod:: dxfwrite.drawing.Drawing.add_view

.. automethod:: dxfwrite.drawing.Drawing.add_viewport

Attributes
----------

.. attribute:: header

  the header section, see :ref:`HEADER`

.. attribute:: blocks

  the blocks section, see :ref:`BLOCK` definition.

usage::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing(name='test.dxf')
    drawing.add_layer('LINES')
    drawing.add(dxf.line((0, 0), (10, 0), layer='LINES')))

    # set header vars, see dxf documentation for header var explanation.
    # set string
    drawing.header['$CLAYER'] = 'CurrentLayer'

    # set int/float
    drawing.header['$ANGBASE'] = 30

    # set 3D Point
    drawing.header['$EXTMIN'] = (0, 0, -10)
    drawing.header['$EXTMAX'] = (100, 100, 50)

    # add a block definition to the drawing
    drawing.blocks.add(blockdef)
