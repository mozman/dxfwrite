#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: dxf entity creation engine, main interface for dxfwrite
# module belongs to package: dxfwrite
# Created: 14.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3
"""
DXFEngine is the dedicated interface to dxfwrite
"""

from dxfwrite.entities import Line, Point, Solid, Face3D, Text, Arc, Circle
from dxfwrite.entities import Trace, Polyline, Polymesh, Polyface
from dxfwrite.entities import Insert, Block, Attdef, Attrib, Shape
from dxfwrite.mtext import MText
from dxfwrite.insert2 import Insert2
from dxfwrite.rect import Rectangle
from dxfwrite.table import Table
from dxfwrite.curves import Ellipse, Spline, Bezier, Clothoid

from dxfwrite.tableentries import Linetype, LinePatternDef, Style, Layer
from dxfwrite.tableentries import View, Viewport, UCS, AppID

class DXFEngine(object):
    """ Factory, creates the dxf objects.

    This is the dedicated interface to dxfwrite, all table entries and all
    all DXF entities shoul be created by the methods of this object.
    All methods are staticmethods, so this object hasn't to be instantiated.
    """

    name = 'DXFWRITE'
    """Engine name for further distinctions of different creation engines."""

    @staticmethod
    def drawing(name='empty.dxf'):
        """Create a new drawing.

        The drawing-object contains all the sections, tables and entities, which
        represent the dxf-drawing.

        For drawing methods see ``drawing.Drawing`` class.
        """
        from dxfwrite.drawing import Drawing
        return Drawing(name)

#--- Table Entries
    @staticmethod
    def layer(name, **kwargs):
        """
        Create a new layer.

        Arguments
        ---------

        name -- layer name  (string)
        flags -- standard flag values, bit-coded, default=0

        =================================  ===================================
                      Flag                             Description
        =================================  ===================================
        STD_FLAGS_LAYER_FROZEN             If set, layer is frozen
        STD_FLAGS_LAYER_FROZEN_BY_DEFAULT  If set, layer is frozen by default
                                           in new Viewports
        STD_FLAGS_LAYER_LOCKED             If set, layer is locked
        =================================  ===================================

        color -- color number (int), negative if layer is off, default=1
        linetype -- linetype name (string), default="CONTINUOUS"
        """
        return Layer(name, **kwargs)

    @staticmethod
    def style(name, **kwargs):
        """
        Create a new textstyle.

        Arguments
        ---------

        name -- textstyle name (string)
        flags -- standard flag values (int), bit-coded, default=0
        generation_flags -- text generation flags (int), default = 0

        =====================  ===================================
                Flag                        Description
        =====================  ===================================
        STYLE_TEXT_BACKWARD    Text is backward (mirrored in X)
        STYLE_TEXT_UPSIDEDOWN  Text is upside down (mirrored in Y)
        =====================  ===================================

        height -- fixed text height, (float), 0 if not fixed = default
        last_height -- last height used (float), default=1.
        width -- width factor (float), default=1.
        oblique -- oblique angle in degree (float), default=0.
        font -- primary font filename (string), default="ARIAL"
        bigfont -- big-font file name(string), default=""
        """
        return Style(name, **kwargs)

    @staticmethod
    def linetype(name, **kwargs):
        """
        Create a new linetype.

        Arguments
        ---------

        name -- linetype name (string)
        flags -- standard flag values, bit-coded, default=0
        description -- descriptive text for linetype (string), default=""
        pattern -- LinePatterDef(), line pattern definition, see method
                   DXFEngine.linepattern()
        """
        return Linetype(name, **kwargs)

    @staticmethod
    def view(name, **kwargs):
        """
        Create a new view.

        Arguments
        ---------

        name -- view name (string)
        flags -- standard flag values (int), bit-coded, default=0
            STD_FLAGS_PAPER_SPACE, if set this is a paper space view.
        height, width --view height and width, in DCS?! (float), default=1.0
        center_point -- view center point, in DCS?! (xy-tuple), default=(.5, .5)
        direction_point -- view direction from target point, in WCS!!
            (xyz-tuple), default=(0, 0, 1)
        target_point -- target point, in WCS!! (xyz-tuple), default=(0, 0, 0)
        lens_length -- lens length (float), default=50
        front_clipping, back_clipping -- front and back clipping planes,
            offsets from target point (float), default=0
        view_twist -- twist angle in degree (float), default=0
        view_mode -- view mode (int), bit-coded, default=0
        =============================
        viewmode flags
        =============================
        VMODE_TURNED_OFF
        VMODE_PERSPECTIVE_VIEW_ACTIVE
        VMODE_FRONT_CLIPPING_ON
        VMODE_BACK_CLIPPING_ON
        VMODE_UCS_FOLLOW_MODE_ON
        VMODE_FRONT_CLIP_NOT_AT_EYE
        =============================
        """
        return View(name, **kwargs)

    @staticmethod
    def viewport(name, **kwargs):
        """
        Create a new viewport.

        Arguments
        ---------

        name -- viewport name (string)
        flags -- standard flag values (int), bit-coded, default=0
        lower_left -- lower-left corner of viewport, (xy-tuple), default=(0, 0)
        upper_right -- upper-right corner of viewport, (xy-tuple), default=(1, 1)
        center_point -- view center point, in WCS, (xy-tuple), default=(.5, .5)
        snap_base -- snap base point, (xy-tuple), default=(0, 0)
        snap_spacing -- snap spacing, X and Y (xy-tuple), default=(.1, .1)
        grid_spacing -- grid spacing, X and Y (xy-tuple), default=(.1, .1)
        direction_point -- view direction from target point (xyz-tuple), default=(0, 0, 1)
        target_point -- view target point (xyz-tuple), default=(0, 0, 0)
        aspect_ratio -- viewport aspect ratio (float), default=1.
        lens_length -- lens length (float), default=50
        front_clipping, back_clipping -- front and back clipping planes, offsets
            from target point (float), default=0
        view_twist -- twist angle in degree (float), default=0
        status -- status field (int), default=0
        id -- id (int), default=0
        circle_zoom -- circle zoom percent (float), default=100
        view_mode -- view mode (int), bit-coded, default=0
        ===============================
        viewmode flags
        ===============================
        VMODE_TURNED_OFF
        VMODE_PERSPECTIVE_VIEW_ACTIVE
        VMODE_FRONT_CLIPPING_ON
        VMODE_BACK_CLIPPING_ON
        VMODE_UCS_FOLLOW_MODE_ON
        VMODE_FRONT_CLIP_NOT_AT_EYE
        ===============================
        fast_zoom -- fast zoom setting (int), default=1
        ucs_icon -- UCSICON settings (int), default=3
        snap_on -- snap on/off (int), default=0
        grid_on -- grid on/off (int), default=0
        snap_style -- snap style (int), defautl=0
        snap_isopair -- snap isopair (int), default=0
        """
        return Viewport(name, **kwargs)

    @staticmethod
    def ucs(name, **kwargs):
        """
        Create a new user-coordinate-system (UCS).

        :param string name: ucs name
        :param int flags: standard flag values, bit-coded
        :param origin: origin in WCS (xyz-tuple), default=(0, 0, 0)
        :param xaxis: xaxis direction in WCS (xyz-tuple), default=(1, 0, 0)
        :param yaxis: yaxis direction in WCS (xyz-tuple), default=(0, 1, 0)

        """
        return UCS(name, **kwargs)

    @staticmethod
    def appid(name):
        return AppID(name)

    @staticmethod
    def linepattern(pattern):
        """Create a LinePatternDef-object from pattern-list.

        example linepattern([2.0, 1.25, -0.25, 0.25, -0.25]), for format
        description see object linepattern.LinePatternDef.
        """
        return LinePatternDef(pattern)

#--- Entities
    @staticmethod
    def line(start=(0., 0.), end=(0., 0.), **kwargs):
        """
        Create a new line-entity of two (3D) points, z-axis is 0 by default.

        :param start: start point (xy- or xyz-tuple)
        :param end: end point (xy- or xyz-tuple)

        """
        return Line(start=start, end=end, **kwargs)

    @staticmethod
    def point(point=(0., 0.), **kwargs):
        """
        Create a new point-entity of one (3D) point, z-axis is 0 by default.

        :param point: start point (xy- or xyz-tuple)
        :param orientation: a 3D vector (xyz-tuple), orientation of PDMODE images ...
            see dxf documtation

        """

        return Point(point=point, **kwargs)

    @staticmethod
    def solid(points=[], **kwargs):
        """
        Create a solid-entity with 3 or 4 sides of (3D) points, z-axis is 0
        by default.

        :param list points: three or four 2D- or 3D-points

        """
        return Solid(points, **kwargs)

    @staticmethod
    def trace(points=[], **kwargs):
        """
        Create a trace-entity with 3 or 4 sides of (3D) points, z-axis is 0
        by default.

        :param points: list of three or four 2D- or 3D-points
        """
        return Trace(points, **kwargs)

    @staticmethod
    def circle(radius=1.0, center=(0., 0.), **kwargs):
        """
        Create a new circle-entity.

        :param float radius: circle radius
        :param center: center point (xy- or xyz-tuple), z-axis is 0 by default

        """
        return Circle(radius=radius, center=center, **kwargs)

    @staticmethod
    def arc(radius=1.0, center=(0., 0.), startangle=0., endangle=360.,
            **kwargs):
        """
        Create a new arc-entity.

        :param float radius: arc radius
        :param center: center point (xy- or xyz-tuple), z-axis is 0 by default
        :param float startangle: start angle in degree
        :param float endangle: end angle in degree
        """
        return Arc(radius=radius, center=center, startangle=startangle,
                   endangle=endangle, **kwargs)

    @staticmethod
    def text(text, insert=(0., 0.), height=1.0, **kwargs):
        """
        Create a new text entity.

        :param string text: the text to display
        :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
        :param float height: text height in drawing-units
        :param float rotation: text rotion in dregree, default=0
        :param float xscale: text width factor, default=1
        :param float oblique: text oblique angle in degree, default=0
        :param string style: text style name, default=STANDARD
        :param int mirror: text generation flags, bit-coded, default=0
        :param int halign: horizontal justification type
        :param int valign: vertical justification type
        :param alignpoint: align point (xy- or xyz-tuple), z-axis is 0 by default
            If the justification is anything other than BASELINE/LEFT,
            alignpoint specify the alignment point (or the second alignment
            point for ALIGN or FIT).

        any combination of **valign** (TOP, MIDDLE, BOTTOM) and **halign** (LEFT,
        CENTER, RIGHT) is valid.

        """
        return Text(text=text, insert=insert, height=height, **kwargs)

    @staticmethod
    def shape(name, insert=(0., 0.), **kwargs):
        """
        Insert a shape-reference.

        :param string name: name of shape
        :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
        :param float xscale: x-scale factor, default=1.
        :param float rotation: rotiation angle in degree, default=0
        :param float oblique: text oblique angle in degree, default=0

        """
        return Shape(name=name, insert=insert, **kwargs)

    @staticmethod
    def insert(blockname, insert=(0., 0.), **kwargs):
        """
        Insert a new block-reference.

        :param string blockname: name of block definition
        :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
        :param float xscale: x-scale factor, default=1.
        :param float yscale: y-scale factor, default=1.
        :param float zscale: z-scale factor, default=1.
        :param float rotation: rotation angle in degree, default=0.
        :param int columns: column count, default=1
        :param int rows: row count, default=1
        :param float colspacing: column spacing, default=0.
        :param float rowspacing: row spacing, default=0.

        """
        return Insert(blockname=blockname, insert=insert, **kwargs)

    @staticmethod
    def attdef(tag, insert=(0., 0.), **kwargs):
        """
        Create a new attribute definition, used in block-definitions.

        :param string text: attribute default text
        :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
        :param string prompt: prompt text, like "insert a value:"
        :param string tag: attribute tag string
        :param int flags: attribute flags, bit-coded, default=0
        :param int length: field length ??? see dxf-documentation
        :param float height: textheight in drawing units (default=1)
        :param float rotation: text rotation (default=0) (all DXF angles in degrees)
        :param float oblique: text oblique angle in degree, default=0
        :param float xscale: width factor (default=1)
        :param string style: textstyle (default=STANDARD)
        :param int mirror: bit coded flags
        :param int halign: horizontal justification type, LEFT, CENTER, RIGHT,
          ALIGN, FIT, BASELINE_MIDDLE (default LEFT)
        :param int valign: vertical justification type, TOP, MIDDLE, BOTTOM,
          BASELINE (default BASELINE)
        :param alignpoint: align point (xy- or xyz-tuple), z-axis is 0 by
          default, if the justification is anything other than BASELINE/LEFT,
          alignpoint specify the alignment point (or the second alignment
          point for ALIGN or FIT).

        """
        return Attdef(tag=tag, insert=insert, **kwargs)

    @staticmethod
    def attrib(text, insert=(0., 0.), **kwargs):
        """
        Create a new attribute, used in the entities section.

        :param string text: attribute text
        :param insert: insert point (xy- or xyz-tuple), z-axis is 0 by default
        :param string tag: attribute tag string
        :param int flags: attribute flags, bit-coded, default=0
        :param int length: field length ??? see dxf-documentation
        :param float height: textheight in drawing units (default=1)
        :param float rotation: text rotation (default=0) (all DXF angles in degrees)
        :param float oblique: text oblique angle in degree, default=0
        :param float xscale: width factor (default=1)
        :param string style: textstyle (default=STANDARD)
        :param int mirror: bit coded flags
        :param int halign: horizontal justification type, LEFT, CENTER, RIGHT,
          ALIGN, FIT, BASELINE_MIDDLE (default LEFT)
        :param int valign: vertical justification type, TOP, MIDDLE, BOTTOM,
          BASELINE (default BASELINE)
        :param alignpoint: align point (xy- or xyz-tuple), z-axis is 0 by
          default, if the justification is anything other than BASELINE/LEFT,
          alignpoint specify the alignment point (or the second alignment
          point for ALIGN or FIT).

        """
        return Attrib(text=text, insert=insert, **kwargs)

    @staticmethod
    def face3d(points=[], **kwargs):
        """
        Create a 3Dface entity with 3 or 4 sides of (3D) points, z-axis is 0
        by default.

        :param points: list of three or four 2D- or 3D-points
        :param int flags: edge flags, bit-coded, default=0

        """
        return Face3D(points, **kwargs)

    @staticmethod
    def block(name, basepoint=(0., 0.), **kwargs):
        """
        Create a block definition, for the blocks section.

        :param string name: blockname
        :param basepoint: block base point (xy- or xyz-tuple), z-axis is 0. by default
        :param int flags: block type flags
        :param string xref: xref pathname

        """
        return Block(name=name, basepoint=basepoint, **kwargs)

    @staticmethod
    def polyline(points=[], **kwargs):
        """
        Create a new polyline entity. Polymesh and polyface are also polylines.

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

        """
        return Polyline(points, **kwargs)

    @staticmethod
    def polymesh(nrows, ncols, **kwargs):
        """
        Create a new polymesh entity.

        nrows and ncols >=2 and <= 256, greater meshes have to be divided into
        smaller meshes.

        The flags-bit **POLYLINE_3D_POLYMESH** is set.

        :param int nrows: count of vertices in m-direction, nrows >=2 and <= 256
        :param int ncols: count of vertices in n-direction, ncols >=2 and <= 256

        """
        return Polymesh(nrows, ncols, **kwargs)

    @staticmethod
    def polyface(precision=6, **kwargs):
        """
        Create a new polyface entity, polyface is a dxf-polyline entity!

        :param precision: vertex-coords will be rounded to precision places, and if
            the vertex is equal to an other vertex, only one vertex will be used,
            this reduces filespace, the coords will be rounded only for the
            comparison of the vertices, the output file has the full float
            resolution.

        """
        return Polyface(precision, **kwargs)

#--- composite entities

    @staticmethod
    def mtext(text, insert, linespacing=1.5, **kwargs):
        """
        Multiline-Text buildup with simple Text-Entities.

        Mostly the same kwargs like text().
        Caution: align point is always the insert point, I don't need a second
        alignpoint because horizontal alignment FIT, ALIGN, BASELINE_MIDDLE is
        not supported.

        linespacing -- linespacing in percent of height, 1.5 = 150% = 1+1/2 lines
        """
        return MText(text, insert, linespacing, **kwargs)

    @staticmethod
    def rectangle(insert, width, height, **kwargs):
        """
        2D Rectangle, build with a polyline and a solid as background filling

        insert point -- where to place the rantangle
        width, height -- in drawing units
        rotation -- in degree (circle = 360 degree)
        halign -- LEFT, CENTER, RIGHT
        valign -- TOP, MIDDLE, BOTTOM
        color -- dxf color index, default is BYLAYER, if color is None, no
             polyline will be created, and the rectangle consist only of the
             background filling (if bgcolor != None)
        bgcolor -- dxf color index, default is None (no background filling)
        layer -- target layer, default is '0'
        linetype -- linetype name, None = BYLAYER
        """
        return Rectangle(insert, width, height, **kwargs)

    @staticmethod
    def table(insert, nrows, ncols, default_grid=True):
        """
        Table object like a HTML-Table, buildup with basic DXF R12 entities.

        Cells can contain Multiline-Text or DXF-BLOCKs, or you can create your own
        cell-type by extending the CustomCell object.
        Cells can span over columns and rows.
        Text cells can contain text with an arbitrary rotation angle, or letters can be
        stacked top-to-bottom.
        BlockCells contains block references (INSERT-entity) created from a block
        definition (BLOCK), if the block definition contains attribute definitions
        (ATTDEF-entity), attribs created by Attdef.new_attrib() will be added to the
        block reference (ATTRIB-entity).

        insert -- insert point as 2D or 3D point
        nrows -- row count
        ncols -- column count
        default_grid -- if True always a a solid line grid will be drawn, if
            False, only explicit defined borders will be drawn, default grid
            has a priority of 50.
        """
        return Table(insert, nrows, ncols, default_grid)

    @staticmethod
    def ellipse(center, radiusx, radiusy, startangle=0., endangle=360.,
                rotation=0., segments=100, **kwargs):
        """
        Create a new ellipse-entity, consisting of an approximation with a
        polyline.

        Arguments
        ---------

        center -- center point (xy- or xyz-tuple), z-axis is 0 by default
        radiusx -- radius in x-axis (float)
        radiusy -- radius in y-axis (float)
        startangle -- in degree (float)
        endangle -- in degree (float)
        rotation -- angle between x-axis and ellipse-main-axis in degree (float)
        segments -- count of line segments for polyline approximation (int)

        Common kwargs
        -------------
        linetype, color, layer
        """
        return Ellipse(center=center, radiusx=radiusx, radiusy=radiusy,
                       startangle=startangle, endangle=endangle, rotation=rotation,
                       segments=segments, **kwargs)

    @staticmethod
    def spline(points, segments=100, **kwargs):
        """
        Create a new cubic-spline-entity, consisting of an approximation with a
        polyline.

        Arguments
        ---------

        points -- breakpoints (knots) as 2D points (float-tuples), defines the
            curve, the curve goes through this points
        segments -- count of line segments for polyline approximation

        Common kwargs
        -------------
        linetype, color, layer
        """
        return Spline(points, segments=segments, **kwargs)

    @staticmethod
    def bezier(**kwargs):
        """
        Create a new cubic-bezier-entity, consisting of an approximation with a
        polyline.

        Methods
        -------
        *start_point(point, tangent) -- set start point and -tangent*

        point -- control point as a 2D point (float-tuple)
        tangent -- control tangent as a 2D vector (float-tuple), 'right' tangent

        *append_point(point, tangent1, tangent2=None, segments=20)*

        Append a control point with two control tangents.

        point -- control point as 2D point
        tangent1 -- first control tangent as 2D vector 'left' of point
        tangent2 -- second control tangent as 2D vector 'right' of point, if
            omitted tangent2 = -tangent1
        segments -- count of line segments for polyline approximation, count of
            line segments from previous control point to this point.

        Common kwargs
        -------------
        linetype, color, layer
        """
        return Bezier(**kwargs)

    @staticmethod
    def clothoid(start=(0, 0), rotation=0., length=1., paramA=1.0,
                 mirrorx=False, mirrory=False, segments=100, **kwargs):
        """
        Create a new clothoid-entity, consisting of an approximation with a
        polyline. see http://en.wikipedia.org/wiki/Euler_spiral

        Arguments
        ---------

        start -- insert point as 2D points (float-tuples)
        rotation -- in dregrees (float)
        length -- length of curve in drawing units (float)
        paramA -- clothoid parameter A
        mirrorx -- True or False
        mirrory -- True or False
        segments -- count of line segments for polyline approximation

        Common kwargs
        -------------
        linetype, color, layer
        """
        return Clothoid(start=start, rotation=rotation, length=length,
                        paramA=paramA, mirrorx=mirrorx, mirrory=mirrory,
                        segments=segments, **kwargs)

    @staticmethod
    def insert2(blockdef, insert=(0., 0.), attribs={}, **kwargs):
        """
        Insert a new block-reference with auto-creating of attribs from attdefs,
        and setting attrib-text by the attribs-dict.

        Arguments
        ---------

        blockdef -- the block definition itself
        insert -- insert point (xy- or xyz-tuple), z-axis is 0 by default
        xscale -- x-scale factor (float), default=1.
        yscale -- y-scale factor (float), default=1.
        zscale -- z-scale factor (float), default=1.
        rotation -- rotation angle in degree (float), default=0.
        attribs -- dict with tag:value pairs, to fill the the attdefs in the
            block-definition. example: {'TAG1': 'TextOfTAG1'}, create and insert
            an attrib from an attdef (with tag-value == 'TAG1'), and set
            text-value of the attrib to value 'TextOfTAG1'.

        multi-insert is not supported.

        Common kwargs
        -------------
        linetype, color, layer
        """
        return Insert2(blockdef=blockdef, insert=insert, attribs=attribs,
                       **kwargs)
