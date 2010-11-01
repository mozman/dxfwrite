.. _`Drawing`:

Drawing
=======

usage::

    from dxfwrite import DXFEngine as dxf
    drawing = dxf.drawing(name='test.dxf')
    drawing.add_layer('LINES')
    drawing.add(dxf.line((0, 0), (10, 0), layer='LINES')))

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

  the header section, see Header

.. attribute:: blocks

  the blocks section, see Blocks

usage::

    # set header vars, see dxf documentation for header var explanation.
    drawing.header.add('VARNAME', dxf.DXFString('VALUE', group_code))
    # add a block definition to the drawing
    drawing.blocks.add(blockdef)
