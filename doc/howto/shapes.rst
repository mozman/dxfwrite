Shapes Management
=================

Prelude::

    from dxfwrite import DXFEngine
    dwg = DXFEngine.drawing('newdrawing.dxf')

How to create new Shapes?
-------------------------

Shapes like :ref:`LINE` or :ref:`CIRCLE`
will be created by the :class:`~dxfwrite.engine.DXFEngine` object. A new created
shape is not automatically added to the drawing, this is done by the
:meth:`~dxfwrite.drawing.Drawing.add` method of the :class:`~dxfwrite.drawing.Drawing`
object.

::

    line = DXFEngine.line( (0, 0), (1, 1) )
    dwg.add(line)

.. seealso:: :class:`~dxfwrite.engine.DXFEngine` for available entities

How to set/get DXF attributes?
------------------------------

This is common to all **basic** DXF entities (not valid for composite entities)::

    # as keyword arguments
    line = DXFEngine.line((0,0), (1,1), layer='TESTLAYER', linetype='DASHED', color=1)

    # or:
    line['layer'] = 'TESTLAYER'
    line['linetype'] = 'DASHED'
    line['color'] = 1
