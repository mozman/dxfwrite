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








