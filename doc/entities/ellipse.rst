.. _Ellipse:

Ellipse
=======

Type: Composite Entity

Ellipse curves are approximated by a :ref:`POLYLINE`.

For an explanation of ellipse curves see Wikipedia:

http://en.wikipedia.org/wiki/Ellipse

.. method:: DXFEngine.ellipse(center, rx, ry, startangle=0., endangle=360., rotation=0., segments=100, **kwargs)

    :param center: center point (xy- or xyz-tuple), z-axis is 0 by default
    :param float rx: radius in x-axis
    :param float ry: radius in y-axis
    :param float startangle: in degree
    :param float endangle: in degree
    :param float rotation: angle between x-axis and ellipse-main-axis in degree
    :param int segments: count of line segments for polyline approximation
    :param string linetype: linetype name, if not defined = **BYLAYER**
    :param string layer: layer name
    :param int color: range [1..255], 0 = **BYBLOCK**, 256 = **BYLAYER**

Example
-------

.. literalinclude:: ../../examples/ellipse.py
   :lines: 20-41

.. image:: ellipse1.png

.. image:: ellipse2.png

.. image:: ellipse3.png

