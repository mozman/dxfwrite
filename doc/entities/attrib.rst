.. _ATTRIB:

ATTRIB
======

Type: Basic DXF R12 entity.

Create a new attribute, attach this attribute to a block-reference that you made
previously.

Attributes are fill-in-the-blank text fields that you can add to your blocks.
When you create a block definition and then insert it several times in a drawing,
all the ordinary geometry (lines, circles, regular text strings, and so on) in
all the instances are exactly identical. Attributes provide a little more
flexibility in the form of text strings that can be different in each block insert.

#. First you have to create the :ref:`ATTDEF`.
#. Next you will create the block and add the :ref:`ATTDEF` with the
   **block.add(attdef)** method.
#. Create a block-reference **blockref=DXFEngine.insert(blockname, insert)** by
   :ref:`INSERT`.
#. Create an **attrib = attdef.new_attrib(kwargs)**
#. Add **attrib** to block-reference by **blockref.add(attrib)**
#. Add **blockref** to the dxf-drawing, **drawing.add(blockref)**

When you create attributes you can put them on their own layer. This makes it
easy to hide them or display them by turning the layer they are on off. This is
handy when you are using attributes to hold information like phone numbers on a
desk floor plan. Sometimes you will want to see, and plot, the desks without the
text.

Probably the most interesting application for attributes is that you can use them
to create tables and reports that accurately reflect the information you have
stored in your blocks, but this works only in CAD Applications, not with dxfwrite.
The process for doing this is somewhat complex and depends on the used CAD-Application.

.. automethod:: dxfwrite.engine.DXFEngine.attrib

Flags
-----

==================================== ===================================================
flag                                 description
==================================== ===================================================
dxfwrite.ATTRIB_IS_INVISIBLE         Attribute is invisible (does not display)
dxfwrite.ATTRIB_IS_CONST             This is a constant Attribute
dxfwrite.ATTRIB_REQUIRE_VERIFICATION Verification is required on input of this Attribute
dxfwrite.ATTRIB_IS_PRESET            Verification is required on input of this Attribute
==================================== ===================================================

Mirror Flags
------------

================= ===================================
flag              description
================= ===================================
dxfwrite.MIRROR_X Text is backward (mirrored in X)
dxfwrite.MIRROR_Y Text is upside down (mirrored in Y)
================= ===================================

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

usage::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing('test.dxf')
    block = dxf.block(name='BLOCK1')
    attdef = dxf.attdef(insert=(.2, .2),
        rotation=30,
        height=0.25,
        text='test',  # default text
        prompt='input text:', # only important for interactive CAD systems
        tag='BLK')
    block.add(attdef)
    drawing.block.add(block) # add block definition to drawing

    # create a block reference
    blockref = dxf.insert(blockname='BLOCK1', insert=(10, 10))

    # create a new attribute, given keywords override the default values from
    # the attrib definition
    attrib = attdef.new_attrib(height=0.18, text='TEST')

    # add the attrib to the block reference, insert has the default value (.2, .2),
    # and insert is relative to block insert point
    blockref.add(attrib, relative=True)
    drawing.add(blockref) # add block reference to drawing
    drawing.save()
