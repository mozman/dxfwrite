.. _SOLID:

SOLID
=====

Type: Basic DXF R12 entity.

Solids are solid-filled 2D outline, a solid can have 3 or 4 points.

.. method:: DXFEngine.solid(points=[], **kwargs):

    :param list points: three or four 2D- or 3D-points


access/assign solid points by index 0, 1, 2 or 3::

    solid[0] = (1.2, 4.3, 3.3)
    solid[1] = (7.2, 2.3, 4.4)

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

Attribs of DXF entities can be changed by the index operator::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing('drawing.dxf')
    solid = dxf.solid([(0, 0), (2, 0), (2, 1), (0, 1)], color=1)
    solid['layer'] = 'solids'
    solid['color'] = 7

    # assign points by index 0, 1, 2, 3
    solid[0] = (1.2, 4.3, 1.9)
    drawing.add(solid)
    drawing.save()

