.. _Drawing:

Drawing
=======

.. class:: Drawing

    The Drawing object manages all the necessary sections, like header, tables
    and blocks. The tables-attribute contains the layers, styles, linetypes and
    other tables.
    
.. method:: Drawing.__init__(name='noname.dxf')

    :param str name: filename of drawing

Methods
-------

.. method:: Drawing.add(entity)

    Add an entity to drawing.

    shortcut for: Drawing.entities.add()

.. method:: Drawing.save

    Write DXF data to file-system.

.. method:: Drawing.saveas(name)

    Set new filename and write DXF data to file-system.

.. method:: Drawing.add_layer(name, **kwargs)

    Define a new layer. For valid keyword args see: :ref:`Layer`

.. method:: Drawing.add_style(name, **kwargs)

    Define a new text-style. For valid keyword args see: :ref:`Textstyle`

.. method:: Drawing.add_linetype(name, **kwargs)

    Define a new linetype. For valid keyword args see: :ref:`Linetype`

.. method:: Drawing.add_view(name, **kwargs)

    Define a new view. For valid keyword args see: :ref:`View`

.. method:: Drawing.add_viewport(name, **kwargs)

    Define a new viewport. For valid keyword args see: :ref:`Vport`

.. method:: Drawing.add_xref(filepath, insert=(0., 0., 0.), layer='0')

    Create a simple XREF reference, `filepath` is the referenced
    drawing and `insert` is the insertion point.

Attributes
----------

.. attribute:: header

  the header section, see :ref:`HEADER`

.. attribute:: modelspace

  Provides only a `add` method for adding entities to the `modelspace`, does the same
  as the :meth:`~Drawing.add` method of the `drawing` object, except
  it garantees the `paper_space` attribute of the added entity is ``'0'``.

.. attribute:: paperspace

  Provides only a `add` method for adding entities to the `paperspace`, does the same
  as the :meth:`~Drawing.add` method of the `drawing` object, except
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

