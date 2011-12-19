.. _MText:

MText
=====

Type: Composite Entity

* Multiline-Text buildup with simple Text-Entities
* Mostly the same kwargs like :ref:`TEXT`
* Lines are separated by ``'\n'``

Caution: align point is always the insert point, I don't need a second alignpoint
because horizontal alignment **FIT**, **ALIGN**, **BASELINE_MIDDLE** is not
supported by MText.

.. method:: DXFEngine.mtext(text, insert, linespacing=1.5, **kwargs)

    :param string text: the text to display
    :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
    :param float linespacing: linespacing in percent of height, 1.5 = 150% =
        1+1/2 lines
    :param float height: text height in drawing-units
    :param float rotation: text rotion in dregree, default=0
    :param float xscale: text width factor, default=1
    :param float oblique: text oblique angle in degree, default=0
    :param string style: text style name, default=STANDARD
    :param int mirror: text generation flags, bit-coded, default=0
    :param int halign: horizontal justification type
    :param int valign: vertical justification type
    :param string layer: layer name
    :param int color: range [1..255], 0 = **BYBLOCK**, 256 = **BYLAYER**


Mirror Flags
------------

==============  ===================================
Flag            Description
==============  ===================================
const.MIRROR_X  Text is backward (mirrored in X)
const.MIRROR_Y  Text is upside down (mirrored in Y)
==============  ===================================

Properties
----------

.. attribute:: MText.lineheight

   Lineheight in drawing units.

Attributes of composite DXF entities can **not** be changed by the index operator,
use normal object attributes instead::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing('drawing.dxf')
    text = dxf.mtext('Line1\nLine2', (1.0, 1.0), height=0.7, rotation=45)
    text.layer = 'TEXT'
    text.color = 7
    drawing.add(text)
    drawing.save()

Example
-------

.. literalinclude:: ../../examples/mtext.py
   :lines: 20-

Various rotation angles:

.. image:: mtext1.png

Different alignment points:

.. image:: mtext2.png
