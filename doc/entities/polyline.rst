.. _POLYLINE:

POLYLINE
========

A polyline is a single object that consists of one or (more usefully) multiple
linear segments. You can create open or closed regular or irregular polylines.

:ref:`POLYMESH` and :ref:`POLYFACE` are also POLYLINE objects.

Polylines are always 3D-polylines, 2D-polylines are not directly
supported, but you can modify the created polylines by clearing the flag
**POLYLINE_3D_POLYLINE** to get a 2D polyline.

.. method:: DXFEngine.polyline(points=[], **kwargs)

    :param points: list of points, 2D or 3D points, z-value of 2D points is 0.
    :param polyline_elevation: polyline elevation (xyz-tuple), z-axis supplies
        elevation, x- and y-axis has to be 0.)
    :param int flags: polyline flags, bit-coded, default=0
    :param float startwidth: default starting width, default=0
    :param float endwidth: default ending width, default=0
    :param int mcount: polygon mesh M vertex count, default=0
    :param int ncount: polygon mesh N vertex count, default=0
    :param int msmooth_density: (if flags-bit POLYLINE_3D_POLYMESH is set)
        smooth surface M density, default=0
    :param int nsmooth_density: (if flags-bit POLYLINE_3D_POLYMESH is set)
        smooth surface N density, default=0
        same values as msmooth_density
    :param int smooth_surface: curves and smooth surface type, default=0
        ??? see dxf-documentation

Common Keyword Arguments for all Basic DXF R12 Entities
-------------------------------------------------------

=================== =========================================================
keyword             description
=================== =========================================================
layer               Layer name as string
linetype            Linetype name as string, if not defined = **BYLAYER**
color               as integer in range [1..255], 0 = **BYBLOCK**,
                    256 = **BYLAYER**
thickness           Thickness as float
paper_space         0 = entity is in model_space, 1 = entity is in
                    paper_space
extrusion_direction 3D Point as tuple(x, y, z) if extrusion direction is not
                    parallel to the World Z axis
=================== =========================================================

Flags
-----

==================================  ====================================
Flag                                Description
==================================  ====================================
POLYLINE_CLOSED                     This is a closed Polyline (or a
                                    polygon mesh closed in the M
                                    direction)
POLYLINE_MESH_CLOSED_M_DIRECTION    equals **POLYLINE_CLOSED**
POLYLINE_CURVE_FIT_VERTICES_ADDED   Curve-fit vertices have been added
POLYLINE_SPLINE_FIT_VERTICES_ADDED  Spline-fit vertices have been added
POLYLINE_3D_POLYLINE                This is a 3D Polyline
POLYLINE_3D_POLYMESH                This is a 3D polygon mesh
POLYLINE_MESH_CLOSED_N_DIRECTION    The polygon mesh is closed in the
                                    N direction
POLYLINE_POLYFACE_MESH              This Polyline is a polyface mesh
POLYLINE_GENERATE_LINETYPE_PATTERN  The linetype pattern is generated
                                    continuously around the vertices of
                                    this Polyline
==================================  ====================================

Smooth Density Flags
--------------------

========================  =============================
Flag                      Description
========================  =============================
POLYMESH_NO_SMOOTH        no smooth surface fitted
POLYMESH_QUADRIC_BSPLINE  quadratic B-spline surface
POLYMESH_CUBIC_BSPLINE    cubic B-spline surface
POLYMESH_BEZIER_SURFACE   Bezier surface
========================  =============================

Methods
-------

.. method:: Polyline.add_vertex(point, **kwargs)

    Add a point to polyline.

    :param point: is a 2D or 3D point, z-value of a 2D point is 0.

.. method:: Polyline.add_vertices(points)

    Add multiple points.

    :param points: list of points, 2D or 3D points, z-value of 2D points is 0.

.. method:: Polyline.close(status=True)

    Close Polyline: first vertex is connected with last vertex.

    :param bool status:  **True** close polyline; **False** open polyline

Example::

    from dxfwrite import DXFEngine as dxf

    polyline= dxf.polyline(linetype='DOT')
    polyline.add_vertices( [(0,20), (3,20), (6,23), (9,23)] )
    drawing.add(polyline)
    drawing.save()

