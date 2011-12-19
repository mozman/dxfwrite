.. _FACE3D:

FACE3D (3DFACE)
===============

Type: Basic DXF R12 entity.

A 3DFace of three or four points.

.. method:: DXFEngine.face3d(points=[], **kwargs)

    :param points: list of three or four 2D- or 3D-points
    :param int flags: edge flags, bit-coded, default=0

access/assign 3dface points by index 0, 1, 2 or 3::

    face3d[0] = (1.2, 4.3, 3.3)
    face3d[1] = (7.2, 2.3, 4.4)

Flags defined in :mod:`dxfwrite.const`

=============================== =====
Name                            Value
=============================== =====
FACE3D_FIRST_EDGE_IS_INVISIBLE  1
FACE3D_SECOND_EDGE_IS_INVISIBLE 2
FACE3D_THIRD_EDGE_IS_INVISIBLE  4
FACE3D_FOURTH_EDGE_IS_INVISIBLE 8
=============================== =====

Common Keyword Arguments for all Basic DXF R12 Entities
-------------------------------------------------------

=================== =========================================================
keyword             description
=================== =========================================================
layer               Layer name as string
linetype            Linetype name as string, if not defined = **BYLAYER**
color               as integer in range [1..255], 0 = **BYBLOCK**,
                    256 = **BYLAYER**
thickness           Thickness as float
paper_space         0 = entity is in model_space, 1 = entity is in
                    paper_space
extrusion_direction 3D Point as tuple(x, y, z) if extrusion direction is not
                    parallel to the World Z axis
=================== =========================================================

Attribs of DXF entities can be changed by the index operator::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing('drawing.dxf')

    # first edge is invisible
    face3d = dxf.face3d([(0, 0), (2, 0), (2, 1), (0, 1)], flags=1)
    face3d['layer'] = 'faces'
    face3d['color'] = 7

    # assign points by index 0, 1, 2, 3
    face3d[0] = (1.2, 4.3, 1.9)
    drawing.add(face3d)
    drawing.save()

