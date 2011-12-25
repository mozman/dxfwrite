.. _viewport:

Viewports
=========

A viewport is a rectangle area, containing a view to the drawing model,
placed in model- or paperspace.

Create a viewport::

    drawing.add_viewport(name, ...)

is a shortcut for::

    viewport = DXFEngine.viewport(name, ...)
    drawing.viewports.add(viewport)

.. method:: DXFEngine.viewport(name, **kwargs)

    :param name: viewport name (string)
    :param flags: standard flag values (int), bit-coded, default=0
    :param lower_left: lower-left corner of viewport, (xy-tuple), default=(0, 0)
    :param upper_right: upper-right corner of viewport, (xy-tuple), default=(1, 1)
    :param center_point: view center point, in WCS, (xy-tuple), default=(.5, .5)
    :param snap_base: snap base point, (xy-tuple), default=(0, 0)
    :param snap_spacing: snap spacing, X and Y (xy-tuple), default=(.1, .1)
    :param grid_spacing: grid spacing, X and Y (xy-tuple), default=(.1, .1)
    :param direction_point: view direction from target point (xyz-tuple), default=(0, 0, 1)
    :param target_point: view target point (xyz-tuple), default=(0, 0, 0)
    :param aspect_ratio: viewport aspect ratio (float), default=1.
    :param lens_length: lens length (float), default=50
    :param front_clipping: front and back clipping planes, offsets
        from target point (float), default=0
    :param back_clipping: see front_clipping
    :param view_twist: twist angle in degree (float), default=0
    :param status: status field (int), default=0
    :param id: id (int), default=0
    :param circle_zoom: circle zoom percent (float), default=100
    :param view_mode: view mode (int), bit-coded, default=0
    :param fast_zoom: fast zoom setting (int), default=1
    :param ucs_icon: UCSICON settings (int), default=3
    :param snap_on: snap on/off (int), default=0
    :param grid_on: grid on/off (int), default=0
    :param snap_style: snap style (int), default=0
    :param snap_isopair: snap isopair (int), default=0

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
