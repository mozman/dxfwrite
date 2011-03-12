.. _ATTDEF:

ATTDEF
======

Type: Basic DXF R12 entity.

Create a new attribute definition, you can use in the
:ref:`block definition <BLOCK>`.

You create an attribute definition, which acts as a placeholder for a
text string that can vary each time you insert the block. You include the
attribute definition when you create the :ref:`block definition <BLOCK>`.
Then each time you :ref:`insert <INSERT>` the block, you can create an new
attribute from the attribute definition and add them to the block-reference.

After you define the attribute definition you can create a new
:ref:`Attrib <ATTRIB>` and insert it into a :ref:`block reference <BLOCK>`,
you can just use the :func:`attdef.new_attrib()` method and change all the
default values preset from the :ref:`ATTDEF` object.

You rarely need to use any of the flags settings (Invisible, Constant, Verify,
or Preset).

.. automethod:: dxfwrite.engine.DXFEngine.attdef

Flags
-----

===========================  ================================================
Flags                        Description
===========================  ================================================
ATTRIB_IS_INVISIBLE          Attribute is invisible (does not display)
ATTRIB_IS_CONST              This is a constant Attribute
ATTRIB_REQUIRE_VERIFICATION  Verification is required on input of
                             this Attribute
ATTRIB_IS_PRESET             Verification is required on input of this
                             Attribute
===========================  ================================================

Mirror Flags
------------

===========================  ================================================
Flags                        Description
===========================  ================================================
dxfwrite.MIRROR_X            Text is backward (mirrored in X)
dxfwrite.MIRROR_Y            Text is upside down (mirrored in Y)
===========================  ================================================

Common Keyword Arguments for all Basic DXF R12 Entities
-------------------------------------------------------

=================== =========================================================
keyword             description
=================== =========================================================
layer               Layer name as string
linetype            Linetype name as string, if not defined = BYLAYER
color               as integer in range [1..255], 0 = BYBLOCK, 256 = BYLAYER
thickness           Thickness as float
paper_space         0 = entity is in model_space, 1 = entity is in
                    paper_space
extrusion_direction 3D Point as tuple(x, y, z) if extrusion direction is not
                    parallel to the World Z axis
=================== =========================================================

Methods
-------

.. automethod:: dxfwrite.entities.Attdef.new_attrib

example::

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
    blockref = dxf.insert(blockname='BLOCK1', insert=(10, 10)) # create a block reference
    # create a new attribute, given keywords override the default values from the attrib definition
    attrib = attdef.new_attrib(height=0.18, text='TEST')
    # add the attrib to the block reference, insert has the default value (.2, .2),
    # and insert is relative to block insert point
    blockref.add(attrib, relative=True)
    drawing.add(blockref) # add block reference to drawing
    drawing.save()
