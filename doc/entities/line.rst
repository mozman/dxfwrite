.. _LINE:

LINE
====

Type: Basic DXF R12 entity.

Draw a single line segment from start point to end point.

.. automethod:: dxfwrite.engine.DXFEngine.line

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
    line = dxf.line((1.2, 3.7), (5.5, 9.7))
    line['layer'] = 'walls'
    line['color'] = 7
    line['start'] = (1.2, 4.3, 1.9)
    drawing.add(line)
    drawing.save()
