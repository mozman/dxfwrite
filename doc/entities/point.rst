.. _POINT:

POINT
=====

Type: Basic DXF R12 entity.

A point simply marks a coordinate. Points are generally used for reference.

.. method:: DXFEngine.point(point=(0., 0.), **kwargs)

    :param point: start point (xy- or xyz-tuple)
    :param orientation: a 3D vector (xyz-tuple), orientation of PDMODE images ...
        see dxf documentation


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
    point = dxf.point((1.0, 1.0))
    point['layer'] = 'points'
    point['color'] = 7
    point['point'] = (2, 3) # int or float
    drawing.add(point)
    drawing.save()

