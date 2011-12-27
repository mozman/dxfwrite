.. _viewport:

VIEWPORT (Entity)
=================

A viewport is a windows containing a view to the drawing model.

You can create a single layout viewport that fits the entire layout or create
multiple layout viewports in the layout.

.. note:: It is important to create layout viewports on their own layer. When you are
    ready to plot, you can turn off the layer and plot the layout without plotting
    the boundaries of the layout viewports.

.. method:: DXFEngine.viewport(center_point, width, height, **kwargs)

    :param center_point: center point of entity in paper space coordinates as (x, y, z) tuple
    :param float width: width in paper space units
    :param float height: height in paper space units
    :param int status: 0 for viewport off, >0 'stacking' order, 1 is the highest
    :param target_view_point: as (x, y, z) tuple, default value is (0, 0, 0)
    :param view_direction_vector:  as (x, y, z) tuple, default value is (0, 0, 1)
    :param float view_twist_angle: in degrees, default value is 0
    :param float view_height: default value is 1
    :param view_center_point: as (x, y) tuple, default value is (0, 0)
    :param float perspective_lens_length:  default value is 50
    :param float front_clip_plane_z_value: default value is 0
    :param float back_clip_plane_z_value: default value is 0
    :param int view_mode: default value is 0
    :param int circle_zoom: default value is 100
    :param int fast_zoom: default value is 1
    :param int ucs_icon: default value is 3
    :param int snap: default value is 0
    :param int grid:  default value is 0
    :param int snap_style: default value is 0
    :param int snap_isopair: default value is 0
    :param float snap_angle: in degrees, default value is 0
    :param snap_base_point: as (x, y) tuple, default value is (0, 0)
    :param snap_spacing: as (x, y) tuple, default value is (0.1, 0.1)
    :param grid_spacing: as (x, y) tuple, default value is (0.1, 0.1)
    :param int hidden_plot: default value is 0

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
