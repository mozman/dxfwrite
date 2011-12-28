.. _CIRCLE:

CIRCLE
======

Type: Basic DXF R12 entity.

A simple circle.

.. method:: DXFEngine.circle(radius=1.0, center=(0., 0.), **kwargs)

    :param float radius: circle radius
    :param center: center point (xy- or xyz-tuple), z-axis is 0 by default

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
    circle = dxf.circle(2.0, (1.0, 1.0))
    circle['layer'] = 'points'
    circle['color'] = 7
    circle['center'] = (2, 3, 7) # int or float
    circle['radius'] = 3.5
    drawing.add(circle)
    drawing.save()

