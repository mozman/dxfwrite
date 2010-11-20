.. TEXT:

TEXT
====

Type: Basic DXF R12 entity.

A simple one line text.

.. automethod:: dxfwrite.engine.DXFEngine.text

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

Mirror Flags
------------

==============  ===================================
Flag            Description
==============  ===================================
const.MIRROR_X  Text is backward (mirrored in X)
const.MIRROR_Y  Text is upside down (mirrored in Y)
==============  ===================================

Attribs of DXF entities can be changed by the index operator::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing('drawing.dxf')
    text = dxf.text('Text', (1.0, 1.0), height=0.7, rotation=45)
    text['layer'] = 'TEXT'
    text['color'] = 7
    drawing.add(text)
    drawing.save()
