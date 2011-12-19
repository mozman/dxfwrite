.. _SHAPE:

SHAPE
=====

Type: Basic DXF R12 entity. (untested)

.. method:: DXFEngine.shape(name, insert=(0., 0.), **kwargs)

    :param string name: name of shape
    :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
    :param float xscale: x-scale factor, default=1.
    :param float rotation: rotation angle in degree, default=0
    :param float oblique: text oblique angle in degree, default=0

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
