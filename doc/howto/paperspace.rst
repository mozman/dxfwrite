.. _paperspace:

Paper space (Layout)
====================

In paper space you assemble your construction work done in model space to
the form as you will print or plot it. In paper space you create
:ref:`viewports <viewport>` to the model space, you can also add headings, text,
a drawing title block, a drawing frame and so on.

The paper space is separated from the model space by the common DXF entity
attribute `paper_space`. If this attribute is ``'0'`` the entity is placed in
model space, if the attribute is ``'1'``, the entity is placed in paper space.

.. note:: In the DXF R12 format exists only **one** paper space.

How to add entities to paper space?
-----------------------------------

Use the `add()` method of the `Drawing` attribute `paperspace` to add
entities to the paper space::

    drawing.paperspace.add(line)

or just set the `paper_space` attribute of the DXF entity, and use the normal
`add()` method of the `Drawing` object::

    line = DXFEngine.line((0,0), (1,1), paper_space=1)
    drawing.add(line)

Model space and paper space units
---------------------------------

I always use the same units for model space and paper space, and because I am not an
experienced AutoCAD user, I don't know if it is possible to choose different units in
model space and paper space. For example: in model space 1 drawing unit = 1 meter, the
paper space units are also in meters, so the paper space area of the DIN A0 paper format
is 1.189 x 0.841 (meter/drawing units).
