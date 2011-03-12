DXFEngine
=========

DXFEngine is the dxf entity creation engine, main interface for dxfwrite.

.. autoclass:: dxfwrite.engine.DXFEngine

Drawing
-------

.. automethod:: dxfwrite.engine.DXFEngine.drawing


Table Entries
-------------

.. automethod:: dxfwrite.engine.DXFEngine.layer
   :noindex:

.. seealso:: :ref:`Layer`

.. automethod:: dxfwrite.engine.DXFEngine.style
   :noindex:

.. seealso:: :ref:`Textstyle`

.. automethod:: dxfwrite.engine.DXFEngine.linetype

.. automethod:: dxfwrite.engine.DXFEngine.linepattern

.. automethod:: dxfwrite.engine.DXFEngine.view

.. automethod:: dxfwrite.engine.DXFEngine.viewport

viewmode flags for **view** and **viewport**:

* VMODE_TURNED_OFF
* VMODE_PERSPECTIVE_VIEW_ACTIVE
* VMODE_FRONT_CLIPPING_ON
* VMODE_BACK_CLIPPING_ON
* VMODE_UCS_FOLLOW_MODE_ON
* VMODE_FRONT_CLIP_NOT_AT_EYE


.. automethod:: dxfwrite.engine.DXFEngine.ucs

.. automethod:: dxfwrite.engine.DXFEngine.appid

DXF R12 Entities
----------------

.. automethod:: dxfwrite.engine.DXFEngine.arc
   :noindex:

.. seealso:: :ref:`ARC`

.. automethod:: dxfwrite.engine.DXFEngine.attdef
   :noindex:

.. seealso:: :ref:`ATTDEF`

.. automethod:: dxfwrite.engine.DXFEngine.attrib
   :noindex:

.. seealso:: :ref:`ATTRIB`

.. automethod:: dxfwrite.engine.DXFEngine.block
   :noindex:

.. seealso:: :ref:`BLOCK`

.. automethod:: dxfwrite.engine.DXFEngine.circle
   :noindex:

.. seealso:: :ref:`CIRCLE`

.. automethod:: dxfwrite.engine.DXFEngine.face3d
   :noindex:

.. seealso:: :ref:`FACE3D`

.. automethod:: dxfwrite.engine.DXFEngine.insert
   :noindex:

.. automethod:: dxfwrite.engine.DXFEngine.line
   :noindex:

.. seealso:: :ref:`LINE`

.. automethod:: dxfwrite.engine.DXFEngine.point
   :noindex:

.. seealso:: :ref:`POINT`

.. automethod:: dxfwrite.engine.DXFEngine.polyline
   :noindex:

.. seealso:: :ref:`POLYLINE`

.. automethod:: dxfwrite.engine.DXFEngine.polymesh
   :noindex:

.. seealso:: :ref:`POLYMESH`

.. automethod:: dxfwrite.engine.DXFEngine.polyface
   :noindex:

.. seealso:: :ref:`POLYFACE`

.. automethod:: dxfwrite.engine.DXFEngine.shape
   :noindex:

.. seealso:: :ref:`SHAPE`

.. automethod:: dxfwrite.engine.DXFEngine.trace
   :noindex:

.. seealso:: :ref:`TRACE`

.. automethod:: dxfwrite.engine.DXFEngine.text
   :noindex:

.. seealso:: :ref:`TEXT`

Composite Entities
------------------

.. automethod:: dxfwrite.engine.DXFEngine.mtext
   :noindex:

.. seealso:: :ref:`MText`

.. automethod:: dxfwrite.engine.DXFEngine.insert2
   :noindex:

.. seealso:: :ref:`Insert2`

.. automethod:: dxfwrite.engine.DXFEngine.rectangle
   :noindex:

.. seealso:: :ref:`Rectangle`

.. automethod:: dxfwrite.engine.DXFEngine.ellipse
   :noindex:

.. seealso:: :ref:`Ellipse`

.. automethod:: dxfwrite.engine.DXFEngine.spline
   :noindex:

.. seealso:: :ref:`Spline`

.. automethod:: dxfwrite.engine.DXFEngine.bezier
   :noindex:

.. seealso:: :ref:`Bezier`

.. automethod:: dxfwrite.engine.DXFEngine.clothoid
   :noindex:

.. seealso:: :ref:`Clothoid`
