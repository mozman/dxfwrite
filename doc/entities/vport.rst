.. _vport:

Viewport
========

.. note:: Viewports in paper space are not supported (yet?), because the Viewport
    **ENTITY** is not supported at this time, this page only describes the
    Viewport **TABLE ENTRIES**.

A viewport is a windows containing a view to the drawing model. You can change
the default view, which will be displayed on opening the drawing with a CAD
program, by adding a viewport named ``'*ACTIVE'``. In AutoCAD you can place
multiple viewports in the main editor window (Left, Right, Top), but don't ask
me how to do this in the DXF file.

Create a viewport::

    drawing.add_vport(name, ...)

is a shortcut for::

    vport = DXFEngine.vport(name, ...)
    drawing.viewports.add(vport)

.. method:: DXFEngine.vport(name, **kwargs)

    :param str name: viewport name
    :param int flags: standard flag values, bit-coded, default=0
    :param lower_left: lower-left corner of viewport, (xy-tuple), default=(0, 0)
    :param upper_right: upper-right corner of viewport, (xy-tuple), default=(1, 1)
    :param center_point: view center point, in WCS, (xy-tuple), default=(.5, .5)
    :param snap_base: snap base point, (xy-tuple), default=(0, 0)
    :param snap_spacing: snap spacing, X and Y (xy-tuple), default=(.1, .1)
    :param grid_spacing: grid spacing, X and Y (xy-tuple), default=(.1, .1)
    :param direction_point: view direction from target point (xyz-tuple), default=(0, 0, 1)
    :param target_point: view target point (xyz-tuple), default=(0, 0, 0)
    :param aspect_ratio: viewport aspect ratio (float), default=1.
    :param float lens_length: lens length, default=50
    :param float front_clipping: front and back clipping planes, offsets
        from target point , default=0
    :param float back_clipping: see front_clipping
    :param float view_twist: twist angle in degree, default=0
    :param float circle_zoom: circle zoom percent, default=100
    :param int view_mode: view mode, bit-coded, default=0
    :param int fast_zoom: fast zoom setting, default=1
    :param int ucs_icon: UCSICON settings, default=3
    :param int snap_on: snap on/off, default=0
    :param int grid_on: grid on/off, default=0
    :param int snap_style: snap style, default=0
    :param int snap_isopair: snap isopair, default=0

View Mode Flags
---------------

================================  =============================================
Flags                             Description
================================  =============================================
VMODE_TURNED_OFF                  viewport is turned off if bit is set
VMODE_PERSPECTIVE_VIEW_ACTIVE     viewport is in perspective mode if bit is set
VMODE_FRONT_CLIPPING_ON           front clipping is on if bit is set
VMODE_BACK_CLIPPING_ON            back clipping is on if bit ist set
VMODE_UCS_FOLLOW_MODE_ON          ???
VMODE_FRONT_CLIP_NOT_AT_EYE       ???
================================  =============================================
