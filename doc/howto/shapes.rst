Shapes Management
=================

Prelude::

    from dxfwrite import DXFEngine
    dwg = DXFEngine.drawing('newdrawing.dxf')

How to create new Shapes?
-------------------------

Shapes like :ref:`LINE` or :ref:`CIRCLE`
will be created by the :class:`DXFEngine` object. A new created
shape is not automatically added to the drawing, this is done by the
:meth:`Drawing.add` method of the :class:`Drawing` object.

::

    line = DXFEngine.line( (0, 0), (1, 1) )
    dwg.add(line)

.. seealso:: :class:`DXFEngine` for available entities

How to set/get DXF attributes?
------------------------------

This is common to all **basic** DXF entities (not valid for composite entities)::

    # as keyword arguments
    line = DXFEngine.line((0,0), (1,1), layer='TESTLAYER', linetype='DASHED', color=1)

    # or:
    line['layer'] = 'TESTLAYER'
    line['linetype'] = 'DASHED'
    line['color'] = 1

Where should the shapes be placed?
----------------------------------

1. You can add the shapes to the drawing, which means adding the shape to the **model space**::

    line = DXFEngine.line((0, 0), (1, 1))
    dwg.add(line)

2. You can add the shape explicit to the **model space** of the drawing::

    dwg.modelspace.add(line)

3. You can add the shape to the **paper space** (layout) of the drawing::

    dwg.paperspace.add(line)

.. note:: The DXF R12 Standard supports only one paper space (layout).

4. You can add the shape to a **BLOCK** definition entity::

    blockdef = DXFEngine.block('testblk')
    blockdef.add(line)

