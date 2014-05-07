.. _INSERT:

INSERT
======

Type: Basic DXF R12 entity.

Insert a new block-reference, for block definitions see :ref:`BLOCK`.

.. method:: DXFEngine.insert(blockname, insert=(0., 0.), **kwargs)

    :param str blockname: name of block definition
    :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
    :param float xscale: x-scale factor, default=1.
    :param float yscale: y-scale factor, default=1.
    :param float zscale: z-scale factor, default=1.
    :param float rotation: rotation angle in degree, default=0.
    :param int columns: column count, default=1
    :param int rows: row count, default=1
    :param float colspacing: column spacing, default=0.
    :param float rowspacing: row spacing, default=0.

Common Keyword Arguments for all Basic DXF R12 Entities
-------------------------------------------------------

=================== =========================================================
keyword             description
=================== =========================================================
layer               Layer name as string
linetype            Linetype name as string, if not defined = `BYLAYER`
color               as integer in range [1..255], 0 = `BYBLOCK`,
                    256 = `BYLAYER`
thickness           Thickness as float
paper_space         0 = entity is in model_space, 1 = entity is in
                    paper_space
extrusion_direction 3D Point as tuple(x, y, z) if extrusion direction is not
                    parallel to the World Z axis
=================== =========================================================

usage::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing('test.dxf')
    block = dxf.block(name='BLOCK1') # create a block-definition
    drawing.block.add(block) # add block-definition to drawing
    blockref = dxf.insert(blockname='BLOCK1', insert=(10, 10)) # create a block-reference
    drawing.add(blockref) # add block-reference to drawing
    drawing.save()

