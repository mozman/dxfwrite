.. _TEXT:

TEXT
====

Type: Basic DXF R12 entity.

A simple one line text.

.. method:: DXFEngine.text(text, insert=(0., 0.), height=1.0, **kwargs)

    :param string text: the text to display
    :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
    :param float height: text height in drawing-units
    :param float rotation: text rotation in degree, default=0
    :param float xscale: text width factor, default=1
    :param float oblique: text oblique angle in degree, default=0
    :param string style: text style name, default=STANDARD
    :param int mirror: text generation flags, bit-coded, default=0
    :param int halign: horizontal justification type
    :param int valign: vertical justification type
    :param alignpoint: align point (xy- or xyz-tuple), z-axis is 0 by default
        If the justification is anything other than BASELINE/LEFT,
        alignpoint specify the alignment point (or the second alignment
        point for ALIGN or FIT).


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

Aligned Text
------------

Attention at aligned Text, if the horizontal align parameter `halign` = ``CENTER``,
``RIGHT``, ``ALIGNED``, ``FIT``, ``BASELINE_MIDDLE`` or the vertical align parameter
`valign` = ``TOP``, ``MIDDLE`` or ``BOTTOM``, the parameter `alignpoint` defines
the text insert point (``CENTER``, ``TOP``, ...) or the second align point
(``FIT``, ``ALIGNED``)::

    from dxfwrite import DXFEngine as dxf
    from dxfwrite.const import CENTER

    drawing = dxf.drawing('drawing.dxf')
    drawing.add(dxf.text('aligned Text', halign=CENTER, alignpoint=(10.0, 5.0)))
    drawing.save()

