.. _DXFTypes:

DXFTypes
========

In normal cases you **don't** get in touch with *DXFTypes*.

.. _DXFList:

DXFList
-------

DXFList can contain every dxf drawing entity. In the usual case DXFList is used
to group lines, arcs, circles and similar entities, also all composite entities
(Table, MText, Rectangle) can be used. Add with **append(entity)** single
entities to the list.

usage::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing()
    entities = DXFList()
    entities.append(dxf.line((0, 0), (10, 0)))
    entities.append(dxf.text('Text'))
    drawing.add(entities)
    drawing.saveas('test.dxf')

.. _DXFString:

DXFString
---------

Create a basic dxf string with the default group code 1.

usage::

   string = DXFString(value='VARNAME', group_code=1)

.. _DXFName:

DXFName
-------

Create a basic dxf string with the default group code 2.

.. _DXFFloat:


DXFFloat
--------

Create a basic dxf float with the default group code 40.

.. _DXFAngle:

DXFAngle
--------

Create a basic dxf float with the default group code 50.

.. _DXFInt:

DXFInt
------

Create a basic dxf integer with the default group code 70.

.. _DXFBool:

DXFBool
-------

Create a basic dxf bool (0 or 1 as integer) with the default group code 290.

.. _DXFPoint:

DXFPoint
--------

Create a basic dxf point., a dxf point consist of three floats with the following
group codes:

 * x-coordinate -- 10+index_shift
 * y-coordinate -- 20+index_shift
 * z-coordinate -- 30+index_shift

Access coordinates by the index operator::

    point = DXFPoint(coords=(x, y, z), index_shift=0)
    x = point['x'] # or point[0]
    y = point['y'] # or point[1]
    z = point['z'] # or point[2]
    x, y = point['xy']
    x, y, z = point['xyz']
    z, y, x = point['zyx']

.. _DXFPoint2D:

DXFPoint2D
----------

like DXFPoint, but only x and y coordinates will be used.

.. _DXFPoint3D:

DXFPoint3D
----------

like DXFPoint, but alway 3 coordinates will be used, z = 0 if omitted.
