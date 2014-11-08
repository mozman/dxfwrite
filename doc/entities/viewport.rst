.. _viewport:

VIEWPORT (Entity)
=================

A viewport is a window showing a part of the model space.

You can create a single layout viewport that fits the entire layout or create
multiple layout viewports in the paper space (layout).

.. note:: It is important to create layout viewports on their own layer. When you are
    ready to plot, you can turn off the layer and plot the layout without plotting
    the boundaries of the layout viewports. `dxfwrite` uses the layer `VIEWPORTS`
    as default layer for viewports.

.. method:: DXFEngine.viewport(center_point, width, height, **kwargs)

    :param center_point: center point of viewport in paper space as (x, y, z) tuple
    :param float width: width of viewport in paper space
    :param float height: height of viewport in paper space
    :param int status: 0 for viewport is off, >0 'stacking' order, 1 is highest priority
    :param view_target_point: as (x, y, z) tuple, default value is (0, 0, 0)
    :param view_direction_vector:  as (x, y, z) tuple, default value is (0, 0, 0)
    :param float view_twist_angle: in radians, default value is 0
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
VMODE_BACK_CLIPPING_ON            back clipping is on if bit is set
VMODE_UCS_FOLLOW_MODE_ON          ???
VMODE_FRONT_CLIP_NOT_AT_EYE       ???
================================  =============================================

Common Keyword Arguments for all Basic DXF R12 Entities
-------------------------------------------------------

=================== =========================================================
keyword             description
=================== =========================================================
layer               Layer name as string
linetype            Linetype name as string, if not defined = `BYLAYER`
color               as integer in range [1..255], 0 = `BYBLOCK`,
                    256 = `BYLAYER`
=================== =========================================================

Model space and paper space units
---------------------------------

.. seealso:: :ref:`paperspace`

Placing the Viewport
--------------------

The location of the viewport in paper space is defined by the parameters `center_point`,
`width` and `height` defines the size of the viewport, all values in paper space
coordinates and units. If viewports are overlapping, the display order is defined by
the `status` parameter (stacking order), viewports with `status=2` are covered by
viewports with `status=1` (`status=1` is the highest display priority). The
viewport is always placed in the paper space by default (`paper_space` parameter
is 1), placing in model space is possible, but does not display any content.

The viewport content
--------------------

The viewport gets the content from the model space, the area to show is defined
by the parameter `view_target_point` and `view_height`, because the aspect
ratio of the viewport is fixed by the parameter `width` and `height`, there is **no**
parameter view_width, all values in model space coordinates and units.

Scaling factor
--------------

Calculate the scaling factor by `height` divided by `view_height`, example: display a 50.0m
model space area in a 1.0m paper space area => 1.0/50.0 => 0.02. If you want a scaling
factor of 1:50 (0.02) and the model space area to display is given,
calculate the necessary viewport height by `view_height/50`, this is correct if the model
space and the paper space has the same drawing units.

Showing 3D content
------------------

- Define the `view_target_point` parameter, this is the point you look at.
- Define the `view_direction_vector`, this is just a direction vector, the
  real location in space is not important.
- The `view_center_point` shifts the viewport,
- and `view_height` determines the model space area to display in the viewport

Example (see also `examples\\viewports_in_paperspace.py`)::

    drawing.add(
        DXFEngine.viewport(
            # location of the viewport in paper space
            center_point=(16, 10),
            # viewport width in paper space
            width=4,
            # viewport height in paper space
            height=4,
            # the model space point you look at
            view_target_point=(40, 40, 0),
            # view_direction_vector determines the view direction,
            # and it just a VECTOR, the view direction is from the location
            # of view_direction_vector to (0, 0, 0)
            view_direction_vector=(-1, -1, 1),
            # now we have a view plane (viewport) with its origin (0, 0) in
            # the view target point and view_center_point shifts
            # the center of the viewport
            view_center_point=(0, 0),
            view_height=30))


.. image:: viewport.png

