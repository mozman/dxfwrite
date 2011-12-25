.. _view:

Views
=====

A view is a named 'look' at the drawing model. This supports users of CAD software
to choose different views at the drawing model. To change the default view, add
a view named ``'*ACTIVE'``.

Create a view::

    drawing.add_view(name, ...)

is a shortcut for::

    view = DXFEngine.view(name, ...)
    drawing.views.add(view)

.. method:: DXFEngine.view(name, **kwargs)

    :param string name: view name
    :param int flags: standard flag values, bit-coded, default=0
        STD_FLAGS_PAPER_SPACE, if set this is a paper space view.
    :param float height, width: view height and width, in DCS?!, default=1.0
    :param center_point: view center point, in DCS?! (xy-tuple), default=(.5, .5)
    :param direction_point: view direction from target point, in WCS!!
        (xyz-tuple), default=(0, 0, 1)
    :param target_point: target point, in WCS!! (xyz-tuple), default=(0, 0, 0)
    :param float lens_length: lens length, default=50
    :param float front_clipping: front and back clipping planes,
        offsets from target point, default=0
    :param back_clipping: see front_clipping
    :param float view_twist: twist angle in degree, default=0
    :param int view_mode: view mode, bit-coded, default=0

View Mode Flags
---------------

================================  ================================================
Flags                             Description
================================  ================================================
VMODE_TURNED_OFF                  ???
VMODE_PERSPECTIVE_VIEW_ACTIVE     ???
VMODE_FRONT_CLIPPING_ON           ???
VMODE_BACK_CLIPPING_ON            ???
VMODE_UCS_FOLLOW_MODE_ON          ???
VMODE_FRONT_CLIP_NOT_AT_EYE       ???
================================  ================================================
