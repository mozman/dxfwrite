.. _Bezier:

Bezier
======

Type: Composite Entity

Bezier curves are approximated by :ref:`POLYLINE`.

For an explanation of bezier curves see Wikipedia:

http://en.wikipedia.org/wiki/B%C3%A9zier_curve

.. automethod:: dxfwrite.engine.DXFEngine.bezier

Methods
-------

.. automethod:: dxfwrite.curves.Bezier.start

.. automethod:: dxfwrite.curves.Bezier.append

Example
-------

.. literalinclude:: ../../examples/bezier.py
   :lines: 21-51

.. image:: bezier.png

