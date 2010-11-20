.. _POLYFACE:

POLYFACE
========

Create a new polyface entity, polyface is a dxf-polyline entity!. A Polyface
consist of one or more faces, where each face can have three or four 3D points.

.. automethod:: dxfwrite.engine.DXFEngine.polyface

=== precision ===
vertex-coords will be rounded to precision places, and if
the vertex is equal to an other vertex, only one vertex will be used,
this reduces filespace, the coords will be rounded only for the
comparison of the vertices, the output file has the full float
resolution.

The flags-bit **POLYLINE_POLYFACE** is set.

for **kwargs** see :ref:`POLYLINE`

Methods
-------

.. automethod:: dxfwrite.entities.Polyface.add_face

Example
-------

.. literalinclude:: ../../examples/polyface.py
   :lines: 23-66

.. image:: faces.png