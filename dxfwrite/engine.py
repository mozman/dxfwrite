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
from dxfwrite.buildups import MText, Rectangle
from dxfwrite.table import Table

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
        from drawing import Drawing
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

        Arguments
        ---------

        name -- ucs name (string)
        flags -- standard flag values, bit-coded
        origin -- origin in WCS (xyz-tuple), default=(0, 0, 0)
        xaxis -- xaxis direction in WCS (xyz-tuple), default=(1, 0, 0)
        yaxis -- yaxis direction in WCS (xyz-tuple), default=(0, 1, 0)
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

        Arguments
        ---------

        start -- start point (xy- or xyz-tuple)
        end -- end point (xy- or xyz-tuple)

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Line(start=start, end=end, **kwargs)

    @staticmethod
    def point(point=(0., 0.), **kwargs):
        """
        Create a new point-entity of one (3D) point, z-axis is 0 by default.

        Arguments
        ---------

        point -- start point (xy- or xyz-tuple)
        orientation -- a 3D vector (xyz-tuple), orientation of PDMODE images ...
            see dxf documtation

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """

        return Point(point=point, **kwargs)

    @staticmethod
    def solid(points=[], **kwargs):
        """
        Create a solid-entity with 3 or 4 sides of (3D) points, z-axis is 0
        by default.

        Arguments
        ---------

        points -- list of three or four 2D- or 3D-points

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Solid(points, **kwargs)

    @staticmethod
    def trace(points=[], **kwargs):
        """
        Create a trace-entity with 3 or 4 sides of (3D) points, z-axis is 0
        by default.

        Arguments
        ---------

        points -- list of three or four 2D- or 3D-points

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Trace(points, **kwargs)

    @staticmethod
    def circle(radius=1.0, center=(0., 0.), **kwargs):
        """
        Create a new circle-entity.

        Arguments
        ---------

        radius -- circle radius (float)
        center -- center point (xy- or xyz-tuple), z-axis is 0 by default

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """

        return Circle(radius=radius, center=center, **kwargs)

    @staticmethod
    def arc(radius=1.0, center=(0., 0.), startangle=0., endangle=360.,
            **kwargs):
        """
        Create a new arc-entity.

        Arguments
        ---------

        radius -- arc radius (float)
        center -- center point (xy- or xyz-tuple), z-axis is 0 by default
        startangle -- start angle in degree (float)
        endangle -- end angle in degree (float)

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Arc(radius=radius, center=center, startangle=startangle,
                   endangle=endangle, **kwargs)

    @staticmethod
    def text(text, insert=(0., 0.), height=1.0, **kwargs):
        """
        Create a new text entity.

        Arguments
        ---------

        text -- the text to display (string)
        insert -- insert point (xy- or xyz-tuple), z-axis is 0 by default
        height -- text height in drawing-units (float)
        rotation -- text rotion in dregree (float), default=0
        xscale -- text width factor (float), default=1
        oblique -- text oblique angle in degree (float), default=0
        style -- text style name (string), default=STANDARD
        mirror -- text generation flags (int), bit-coded, default=0
        ==============  ===================================
        const.MIRROR_X  Text is backward (mirrored in X)
        const.MIRROR_Y  Text is upside down (mirrored in Y)
        ==============  ===================================
        halign -- horizontal justification type (int)
        valign -- vertical justification type (int)

        any combination of valign (TOP, VMIDDLE, BOTTOM) and halign(LEFT,
        CENTER, RIGHT) is valid.

        alignpoint -- align point (xy- or xyz-tuple), z-axis is 0 by default
            If the justification is anything other than BASELINE/LEFT,
            alignpoint specify the alignment point (or the second alignment
            point for ALIGN or FIT).

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Text(text=text, insert=insert, height=height, **kwargs)

    @staticmethod
    def shape(name, insert=(0., 0.), **kwargs):
        """
        Insert a shape-reference.

        Arguments
        ---------

        name -- name of shape (string)
        insert -- insert point (xy- or xyz-tuple), z-axis is 0 by default
        xscale -- x-scale factor (float), default=1.
        rotation -- rotiation angle in degree (float), default=0
        oblique -- text oblique angle in degree (float), default=0

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Shape(name=name, insert=insert, **kwargs)

    @staticmethod
    def insert(blockname, insert=(0., 0.), **kwargs):
        """
        Insert a new block-reference.

        Arguments
        ---------

        blockname -- name of block definition (string)
        insert -- insert point (xy- or xyz-tuple), z-axis is 0 by default
        xscale -- x-scale factor (float), default=1.
        yscale -- y-scale factor (float), default=1.
        zscale -- z-scale factor (float), default=1.
        rotation -- rotiation angle in degree (float), default=0.
        columns -- column count (int), default=1
        rows -- row count (int), default=1
        colspacing -- column spacing (float), default=0.
        rowspacing -- row spacing (float), default=0.

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Insert(blockname=blockname, insert=insert, **kwargs)

    @staticmethod
    def attdef(text, insert=(0., 0.), **kwargs):
        """
        Create a new attribute definition, used in block-definitions.

        Arguments
        ---------

        text -- attribute default text (string)
        insert -- insert point (xy- or xyz-tuple), z-axis is 0 by default
        prompt -- prompt text (string), like "insert a value:"
        tag -- attribute tag string (string)
        flags -- attribute flags (int), bit-coded, default=0
        ===========================  ===============================
        Flags                        Description
        ===========================  ===============================
        ATTRIB_IS_INVISIBLE          Attribute is invisible (does not display)
        ATTRIB_IS_CONST              This is a constant Attribute
        ATTRIB_REQUIRE_VERIFICATION  Verification is required on input of
                                     this Attribute
        ATTRIB_IS_PRESET             Verification is required on input of this
                                     Attribute
        ===========================  ===============================
        length -- field length (int) ??? see dxf-documentation
        rotation, xscale, oblique, style -- see text method
        mirror, halign , valign, alignpoint -- see text method

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Attdef(text=text, insert=insert, **kwargs)

    @staticmethod
    def attrib(text, insert=(0., 0.), **kwargs):
        """
        Create a new attribute, used in the entities section.

        Arguments
        ---------
        like attdef, but without prompt

        text -- attribute text (string)
        """
        return Attrib(text=text, insert=insert, **kwargs)

    @staticmethod
    def face3d(points=[], **kwargs):
        """
        Create a 3Dface entity with 3 or 4 sides of (3D) points, z-axis is 0
        by default.

        Arguments
        ---------

        points -- list of three or four 2D- or 3D-points
        flags -- edge flags (int), bit-coded, default=0
        ===============================
        FACE3D_FIRST_EDGE_IS_INVISIBLE
        FACE3D_SECOND_EDGE_IS_INVISIBLE
        FACE3D_THIRD_EDGE_IS_INVISIBLE
        FACE3D_FOURTH_EDGE_IS_INVISIBLE
        ===============================

        Common kwargs
        -------------
        linetype, color, layer, elevation, thickness, paper_space,
        extrusion_direction (see doc-string DXFEngine)
        """
        return Face3D(points, **kwargs)

    @staticmethod
    def block(name, basepoint=(0., 0.), **kwargs):
        """
        Create a block definition, for the blocks section.

        Add block to a drawing: drawing.blocks.add(block-object)
        Find block-definitions: drawing.blocks.find(blockname)

        Add entities to a block: block.add(entity), where entity can be every
        drawing entity like circle, line, polyline, attribute, text, ...

        Arguments
        ---------

        name -- blockname (string)
        basepoint -- block base point (xy- or xyz-tuple), z-axis is 0. by default
        flags -- block type flags
        ===========================  ===========================================
        BLK_ANONYMOUS                This is an anonymous block generated by
                                     hatching, associative dimensioning, other
                                     internal operations, or an application
        BLK_NON_CONSTANT_ATTRIBUTES  This block has non-constant attribute
                                     definitions (this bit is not set if the
                                     block has any attribute definitions that
                                     are constant, or has no attribute
                                     definitions at all)
        BLK_XREF                     This block is an external reference (xref)
        BLK_XREF_OVERLAY             This block is an xref overlay
        BLK_EXTERNAL                 This block is externally dependent
        BLK_RESOLVED                 This is a resolved external reference, or
                                     dependent of an external reference (ignored
                                     on input)
        BLK_REFERENCED               This definition is a referenced external
                                     reference (ignored on input)
        xref -- xref pathname (string)

        Common kwargs
        -------------
        linetype, color, layer, elevation?, thickness?, paper_space?,
        extrusion_direction? (see doc-string DXFEngine)

        linetype, color, layer are used by block-elements with BYBLOCK
        """
        return Block(name=name, basepoint=basepoint, **kwargs)

    @staticmethod
    def polyline(points=[], **kwargs):
        """
        Create a new polyline entity. Polymesh and polyface are also polylines.

        dxfwrite polylines are always 3D-polylines, 2D-polylines are not directly
        supported, but you can modify the created polylines by clearing the
        flag ``POLYLINE_3D_POLYLINE`` to get a 2D polyline.

        points -- list of 3D or 2D points (xy- or xyz-tuples), default z-value
            for 2d points is 0.

        see Polyline object:
        * polyline.add_vertex(point)
        * polyline.add_vertices([points])
        * polyline.close(Bool)

        KWARGS

        polyline_elevation -- polyline elevation (xyz-tuple), z-axis supplies
            elevation, x- and y-axis has to be 0.)
        flags -- polyline flags, bit-coded, default=0
        ==================================  ====================================
        POLYLINE_CLOSED                     This is a closed Polyline (or a
                                            polygon mesh closed in the M
                                            direction)
        POLYLINE_MESH_CLOSED_M_DIRECTION    equals POLYLINE_CLOSED
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

        startwidth -- default starting width (float), default=0
        endwidth -- default ending width (float), default=0
        mcount -- polygon mesh M vertex count (int), default=0
        ncount -- polygon mesh N vertex count (int), default=0
        msmooth_density -- (if flags-bit POLYLINE_3D_POLYMESH is set)
            smooth surface M density (int), default=0
        ========================  =============================
        POLYMESH_NO_SMOOTH        no smooth surface fitted
        POLYMESH_QUADRIC_BSPLINE  quadratic B-spline surface
        POLYMESH_CUBIC_BSPLINE    cubic B-spline surface
        POLYMESH_BEZIER_SURFACE   Bezier surface
        ========================  =============================
        nsmooth_density -- (if flags-bit POLYLINE_3D_POLYMESH is set)
            smooth surface N density, (int), default=0
            same values as msmooth_density
        smooth_surface -- curves and smooth surface type (int), default=0
            ??? see dxf-documentation

        Common kwargs
        -------------
        linetype, color, layer, elevation?, thickness?, paper_space,
        extrusion_direction? (see doc-string DXFEngine)
        """
        return Polyline(points, **kwargs)

    @staticmethod
    def polymesh(nrows, ncols, **kwargs):
        """
        Create a new polymesh entity, polymesh is a dxf-polyline entity!

        nrows and ncols >=2 and <= 256, greater meshes have to be divided into
        smaller meshes.

        flags-bit POLYLINE_3D_POLYMESH is set.
        see Polymesh object:
        * polymesh.set_vertex(row, col, xyz-tuple)
        * polymesh.set_mclosed()
        * polymesh.set_nclosed()

        Arguments
        ---------
        see polyline
        """
        return Polymesh(nrows, ncols, **kwargs)

    @staticmethod
    def polyface(precision=6, **kwargs):
        """
        Create a new polyface entity, polyface is a dxf-polyline entity!

        precision --vertex-coords will be rounded to precision places, and if
            the vertex is equal to an other vertex, only one vertex will be used,
            this reduces filespace, the coords will be rounded only for the
            comparison of the vertices, the output file has the full float
            resolution.

        flags-bit POLYLINE_POLYFACE is set.
        see Polyface object:
        * polyface.add_face(vertices, color)
        * vertices is a list of 3 or 4 xyz-tuples

        Arguments
        ---------
        see polyline
        """
        return Polyface(precision, **kwargs)

#--- Buildups

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

        insert point --where to place the rantangle
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
        return Table(insert, nrows, ncols, default_grid)