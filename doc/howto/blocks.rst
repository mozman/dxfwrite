Blocks Management
=================

A block is a collection of objects grouped together to form a single object.
All supported dxf entities can also be added to block like to a drawing.

Prelude::

    from dxfwrite import DXFEngine
    dwg = DXFEngine.drawing('newdrawing.dxf')

How to create a new block?
--------------------------

Just the blockname is required::

    block = DXFEngine.block(name='rect')

How to add shapes to the block?
-------------------------------

every supported shape can be added::

    block.add(DXFEngine.rect((0, 0), width=3, height=3))

How use the block?
------------------

To use the block, insert the block by the :ref:`INSERT` entity::

    dwg.add(DXFEngine.insert('rect', insert=(10,10)))

What is the basepoint?
----------------------

The basepoint are the block coordinates, where the block will be placed by
the insertion point of the :ref:`INSERT` entity.

How to use attributes?
----------------------

Attributes are fill-in-the-blank text fields that you can add to your blocks.
When you insert a block several times in a drawing,
all the ordinary geometry (lines, circles, regular text strings, and so on) in
all the instances are exactly identical. Attributes provide a little more
flexibility in the form of text strings that can be different in each block insert.

::

    # 1. create the ATTDEF
    name = DXFEngine.attdef(tag='NAME', insert=(2, 2))
    # 2. add the ATTDEF with the block
    block.add(name)

Using INSERT
~~~~~~~~~~~~

::

    # 3. create a block-reference
    blockref = DXFEngine.insert('rect', insert=(10,10))
    # 4. create an ATTRIB, text is the ATTRIB content to display
    nameattrib = name.new_attrib(text='Rect')
    # 5. add ATTRIB to the block-reference
    blockref.add(nameattrib)
    # 6. add block-reference to dxf-drawing
    dwg.add(blockref)

Using INSERT2
~~~~~~~~~~~~~

Simplified usage of attribs::

    # 3. create a block-reference by insert2
    # attribs = { key: value, ... }, key=ATTDEF-tag, value=ATTRIB-text
    # but you have to use the block defintion
    blockref = DXFEngine.insert2(block, insert=(10,10), attribs={'NAME': 'Rect'})
    # 4. add block-reference to dxf-drawing
    dwg.add(blockref)

