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

.. automethod:: dxfwrite.drawing.Drawing.add_xref

Attributes
----------

.. attribute:: header

  the header section, see :ref:`HEADER`

.. attribute:: modelspace

  Provides only a `add` method for adding entities to the `modelspace`, does the same
  as the :meth:`~dxfwrite.drawing.Drawing.add` method of the `drawing` object, except
  it garantees the `paper_space` attribute of the added entity is ``'0'``.

.. attribute:: paperspace

  Provides only a `add` method for adding entities to the `paperspace`, does the same
  as the :meth:`~dxfwrite.drawing.Drawing.add` method of the `drawing` object, except
  it garantees the `paper_space` attribute of the added entity is ``'1'``.

.. warning:: DXF R12 supports only **one** paperspace.

usage::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing(name='test.dxf')
    drawing.paperspace.add(dxf.text('Text in paperspace'))
    drawing.modelspace.add(dxf.text('Text in modelspace'))
    drawing.add(dxf.text('Text also in paperspace', insert=(0, 1), paper_space=1))
    drawing.add(dxf.text('Text also in modelspace', insert=(0, 1)))


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
