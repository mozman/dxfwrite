#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: dxf entity creation engine, main interface for dxfwrite
# module belongs to package: dxfwrite
# Created: 14.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

""" module: engine, implements the DXFEngine-object

DXFEngine is the dxf entity creation engine, main interface for dxfwrite
"""

from dxfwrite.entities import Line, Point, Solid, Face3D, Text, Arc, Circle
from dxfwrite.entities import Polyline, Polymesh, Polyface
from dxfwrite.entities import Insert, Block, Attdef, Attrib, Shape
from dxfwrite.buildups import MText

from dxfwrite.tableentries import Linetype, LinePatternDef, Style, Layer
from dxfwrite.tableentries import View, Viewport, UCS, AppID

class DXFEngine(object):
    """ Factory, creates the dxf objects.

    METHODS

    drawing
        creates a new drawing

*** create table entries ***

    layer
        creates a new layer 'name'
    style
        creates a new text style 'name'
    linetype
        creates a new linetype 'name'
    view
        creates a new view 'name'
    viewport
        creates a new viewport 'name'

*** create drawings entities ***

    line
        creates a new LINE object
    point
        creates a new POINT object
    solid
        creates a new SOLID object with corner points=[list of points]
        points are tuples (x, y) or (x, y, z)
    circle
        creates a new CIRCLE object
    arc
        creates a new ARC object
    text
        creates a new TEXT object
    shape
        creates a new SHAPE object
    insert
        creates a new INSERT object
    attdef
        creates a new ATTDEF object
    attrib
        creates a new ATTRIB object
    face3d
        creates a new 3DFACE with corner points=[list of points], **kwargs
        points are tuples (x, y) or (x, y, z)
    block
        creates a new BLOCK object (add manually to section BLOCKS!)
        drawing.blocks.add(block)
    polyline
        creates a 3D polyline
    polymesh
        creates a m,n 3D polymesh
    polyface
        creates a 3D polyfaces, with arbitrary amount of faces with 3 or 4 points.

*** COMMON KWARGS for all drawing entities:

    linetype
        linetype name (string)
    color
        colorindex (0-255) (int)
    layer
        layer name (string)
    elevation
        (float)
    thickness
        (float)
    paper_space
        (int) 1 if object is in paper space, else 0
    extrusion_direction
        (xyz-tuple)
    """
    name = 'DXFWRITE'

    @staticmethod
    def drawing(name='empty.dxf'):
        from drawing import Drawing
        return Drawing(name)

#--- Table Entries
    @staticmethod
    def layer(name, **kwargs):
        """ create a new layer

        name
            layer name  (string)

        KWARGS:

        flags
            standard flag values, bit-coded, default=0
            STD_FLAGS_LAYER_FROZEN = If set, layer is frozen
            STD_FLAGS_LAYER_FROZEN_BY_DEFAULT = If set, layer is frozen by
                default in new Viewports
            STD_FLAGS_LAYER_LOCKED = If set, layer is locked
        color
            color number (int), negative if layer is off, default=1
        linetype
            linetype name (string), default="CONTINUOUS"

        """
        return Layer(name, **kwargs)

    @staticmethod
    def style(name, **kwargs):
        """ create a new textstyle

        name
           textstyle name (string)

        KWARGS:

        flags
            standard flag values (int), bit-coded, default=0
        generation_flags
            text generation flags (int), default = 0
            STYLE_TEXT_BACKWARD = Text is backward (mirrored in X)
            STYLE_TEXT_UPSIDEDOWN = Text is upside down (mirrored in Y)
        height
            fixed text height, (float), 0 if not fixed = default
        last_height
            last height used (float), default=1.
        width
            width factor (float), default=1.
        oblique
            oblique angle in degree (float), default=0.
        font
            primary font filename (string), default="ARIAL"
        bigfont
            big-font file name(string), default=""
        """
        return Style(name, **kwargs)

    @staticmethod
    def linetype(name, **kwargs):
        """ create a new linetype

        name
           linetype name (string)

        KWARGS:

        flags
            standard flag values, bit-coded, default=0
        description
            descriptive text for linetype (string), default=""
        pattern
            LinePatterDef(), line pattern definition
            see method DXFEngine.linepattern()
        """
        return Linetype(name, **kwargs)

    @staticmethod
    def view(name, **kwargs):
        """ create a new view

        name
           view name (string)

        KWARGS:

        flags
            standard flag values (int), bit-coded, default=0
            STD_FLAGS_PAPER_SPACE, if set this is a paper space view.
        height, width
            view height and width, in DCS?! (float), default=1.0
        center_point
            view center point, in DCS?! (xy-tuple), default = (.5, .5)
        direction_point
            view direction from target point, in WCS!! (xyz-tuple), default=(0, 0, 1)
        target_point
            target point, in WCS!! (xyz-tuple), default=(0, 0, 0)
        lens_length
            lens length (float), default=50
        front_clipping, back_clipping
            front and back clipping planes - offsets from target point (float)
            default=0
        view_twist
            twist angle in degree (float), default=0
        view_mode
            view mode (int), bit-coded, default=0
            VMODE_TURNED_OFF
            VMODE_PERSPECTIVE_VIEW_ACTIVE
            VMODE_FRONT_CLIPPING_ON
            VMODE_BACK_CLIPPING_ON
            VMODE_UCS_FOLLOW_MODE_ON
            VMODE_FRONT_CLIP_NOT_AT_EYE
        """
        return View(name, **kwargs)

    @staticmethod
    def viewport(name, **kwargs):
        """ create a new viewport

        name
           viewport name (string)

        KWARGS:

        flags
            standard flag values (int), bit-coded, default=0
        lower_left
            lower-left corner of viewport, (xy-tuple), default=(0, 0)
        upper_right
            upper-right corner of viewport, (xy-tuple), default=(1, 1)
        center_point
            view center point, in WCS, (xy-tuple), default=(.5, .5)
        snap_base
            snap base point, (xy-tuple), default=(0, 0)
        snap_spacing
            snap spacing, X and Y (xy-tuple), default=(.1, .1)
        grid_spacing
            grid spacing, X and Y (xy-tuple), default=(.1, .1)
        direction_point
            view direction from target point (xyz-tuple), default=(0, 0, 1)
        target_point
            view target point (xyz-tuple), default=(0, 0, 0)
        aspect_ratio
            viewport aspect ratio (float), default=1.
        lens_length
            lens length (float), default=50
        front_clipping, back_clipping
            front and back clipping planes - offsets from target point (float)
            default=0
        view_twist
            twist angle in degree (float), default=0
        status
            status field (int), default=0
        id
            id (int), default=0
        circle_zoom
            circle zoom percent (float), default=100
        view_mode
            view mode (int), bit-coded, default=0
            VMODE_TURNED_OFF
            VMODE_PERSPECTIVE_VIEW_ACTIVE
            VMODE_FRONT_CLIPPING_ON
            VMODE_BACK_CLIPPING_ON
            VMODE_UCS_FOLLOW_MODE_ON
            VMODE_FRONT_CLIP_NOT_AT_EYE
        fast_zoom
            fast zoom setting (int), default=1
        ucs_icon
            UCSICON settings (int), default=3
        snap_on
            snap on/off (int), default=0
        grid_on
            grid on/off (int), default=0
        snap_style
            snap style (int), defautl=0
        snap_isopair
            snap isopair (int), default=0
        """
        return Viewport(name, **kwargs)

    @staticmethod
    def ucs(name, **kwargs):
        """ create a new user-coordinate-system (UCS)

        name
           ucs name (string)

        KWARGS:

        flags
            standard flag values, bit-coded
        origin
            origin in WCS (xyz-tuple), default=(0, 0, 0)
        xaxis
            xaxis direction in WCS (xyz-tuple), default=(1, 0, 0)
        yaxis
            yaxis direction in WCS (xyz-tuple), default=(0, 1, 0)
        """
        return UCS(name, **kwargs)

    @staticmethod
    def appid(name):
        return AppID(name)

    @staticmethod
    def linepattern(pattern):
        """ create a LinePatternDef-object from pattern-list.

        example linepattern([2.0, 1.25, -0.25, 0.25, -0.25]), for format
        description see object linepattern.LinePatternDef.
        """
        return LinePatternDef(pattern)

#--- Entities
    @staticmethod
    def line(start=(0., 0.), end=(0., 0.), **kwargs):
        """ create a new line-entity of two (3D) points, z-axis is 0. by default

        KWARGS:

        start
            start point (xy- or xyz-tuple)
        end
            end point (xy- or xyz-tuple)

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """
        return Line(start=start, end=end, **kwargs)

    @staticmethod
    def point(point=(0., 0.), **kwargs):
        """ create a new point-entity of one (3D) point, z-axis is 0. by default

        KWARGS:

        point
            start point (xy- or xyz-tuple)
        orientation ???
            a 3D vector (xyz-tuple), orientation of PDMODE images ...
            see dxf documtation

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """

        return Point(point=point, **kwargs)

    @staticmethod
    def solid(points=[], **kwargs):
        """ create a solid-entity with 3 or 4 sides of (3D) points, z-axis is
        0. by default

        KWARGS:

        points
            list of three or four 2D- or 3D-points

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """
        return Solid(points, **kwargs)

    @staticmethod
    def circle(radius=1.0, center=(0., 0.), **kwargs):
        """ create a new circle-entity

        KWARGS:

        radius
            circle radius (float)
        center
            center point (xy- or xyz-tuple), z-axis is 0. by default

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """

        return Circle(radius=radius, center=center, **kwargs)

    @staticmethod
    def arc(radius=1.0, center=(0., 0.), startangle=0., endangle=360.,
            **kwargs):
        """ create a new arc-entity

        KWARGS:

        radius
            arc radius (float)
        center
            center point (xy- or xyz-tuple), z-axis is 0. by default
        startangle
            start angle in degree (float)
        endangle
            end angle in degree (float)

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """
        return Arc(radius=radius, center=center, startangle=startangle,
                   endangle=endangle, **kwargs)

    @staticmethod
    def text(text, insert=(0., 0.), height=1.0, **kwargs):
        """ create a new text entity

        KWARGS:

        text
            the text to display (string)
        insert
            insert point (xy- or xyz-tuple), z-axis is 0. by default
        height
            text height in drawing-units (float)
        rotation
            text rotion in dregree (float), default=0.
        xscale
            text width factor (float), default=1.
        oblique
            text oblique angle in degree (float), default=0.
        style
            text style name (string), default=STANDARD
        mirror
            text generation flags (int), bit-coded, default=0
            const.MIRROR_X = Text is backward (mirrored in X)
            const.MIRROR_Y = Text is upside down (mirrored in Y)
        halign
            horizontal justification type (int)
        valign
            vertical justification type (int)

            any combination of valign (TOP, VMIDDLE, BOTTOM) and halign(LEFT,
            CENTER, RIGHT) is valid.

            valign TOP, MIDDLE, BOTTOM:
            LEFT, CENTER, RIGHT: text will be insert at the alignpoint.

            valign BASELINE:
            LEFT: text will be insert at the insert point. (!!!)
            RIGHT, CENTER, BASELINE_MIDDLE: alignpoint specifies the insert point
            ALIGNED: text is aligned between insert and alignpoint
            FIT: text is fitted between insert and alignpoint

        alignpoint
            align point (xy- or xyz-tuple), z-axis is 0. by default
            If the justification is anything other than BASELINE/LEFT,
            alignpoint specify the alignment point (or the second alignment
            point for ALIGN or FIT).

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """
        return Text(text=text, insert=insert, height=height, **kwargs)

    @staticmethod
    def shape(name, insert=(0., 0.), **kwargs):
        """ insert a shape-reference

        KWARGS:

        name
            name of shape (string)
        insert
            insert point (xy- or xyz-tuple), z-axis is 0. by default
        xscale
            x-scale factor (float), default=1.
        rotation
            rotiation angle in degree (float), default=0.
        oblique
            text oblique angle in degree (float), default=0.

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """
        return Shape(name=name, insert=insert, **kwargs)

    @staticmethod
    def insert(blockname, insert=(0., 0.), **kwargs):
        """ insert a new block-reference

        KWARGS:

        blockname
            name of block definition (string)
        insert
            insert point (xy- or xyz-tuple), z-axis is 0. by default
        xscale
            x-scale factor (float), default=1.
        yscale
            y-scale factor (float), default=1.
        zscale
            z-scale factor (float), default=1.
        rotation
            rotiation angle in degree (float), default=0.
        columns
            column count (int), default=1
        rows
            row count (int), default=1
        colspacing
            column spacing (float), default=0.
        rowspacing
            row spacing (float), default=0.

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """
        return Insert(blockname=blockname, insert=insert, **kwargs)

    @staticmethod
    def attdef(text, insert=(0., 0.), **kwargs):
        """ create a new attribute definition, used in block-definitions.

        KWARGS:

        text
            attribute default text (string)
        insert
            insert point (xy- or xyz-tuple), z-axis is 0. by default
        prompt
            prompt text (string), like "insert a value:"
        tag
            attribute tag string (string)
        flags
            attribute flags (int), bit-coded, default=0
            ATTRIB_IS_INVISIBLE = Attribute is invisible (does not display)
            ATTRIB_IS_CONST = This is a constant Attribute
            ATTRIB_REQUIRE_VERIFICATION = Verification is required on input of
            this Attribute
            ATTRIB_IS_PRESET = Verification is required on input of this Attribute
        length
            field length (int) ??? see dxf-documentation
        rotation
            see text
        xscale
            see text
        oblique
            see text
        style
            see text
        mirror
            see text
        halign
            see text
        valign
            see text
        alignpoint
            see text

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)

        """
        return Attdef(text=text, insert=insert, **kwargs)

    @staticmethod
    def attrib(text, insert=(0., 0.), **kwargs):
        """ create a new attribute, used in the entities section

        KWARGS: like attdef, but without prompt

        text
            attribute text (string)
        """
        return Attrib(text=text, insert=insert, **kwargs)

    @staticmethod
    def face3d(points=[], **kwargs):
        """ create a 3Dface entity with 3 or 4 sides of (3D) points, z-axis is
        0. by default

        KWARGS:

        points
            list of three or four 2D- or 3D-points
        flags
            edge flags (int), bit-coded, default=0
            FACE3D_FIRST_EDGE_IS_INVISIBLE
            FACE3D_SECOND_EDGE_IS_INVISIBLE
            FACE3D_THIRD_EDGE_IS_INVISIBLE
            FACE3D_FOURTH_EDGE_IS_INVISIBLE

        common kwargs
             linetype, color, layer, elevation, thickness, paper_space,
             extrusion_direction (see doc-string DXFEngine)
        """
        return Face3D(points, **kwargs)

    @staticmethod
    def block(name, basepoint=(0., 0.), **kwargs):
        """ create a block definition, for the blocks section.

        Add block to a drawing: drawing.blocks.add(block-object)
        Find block-definitions: drawing.blocks.find(blockname)

        Add entities to a block: block.add(entity), where entity can be every
        drawing entity like circle, line, polyline, attribute, text, ...

        KWARGS:

        name
            blockname (string)
        basepoint
            block base point (xy- or xyz-tuple), z-axis is 0. by default
        flags
            block type flags
            BLK_ANONYMOUS = This is an anonymous block generated by hatching,
                associative dimensioning, other internal operations, or an
                application
            BLK_NON_CONSTANT_ATTRIBUTES = This block has non-constant attribute
                definitions (this bit is not set if the block has any attribute
                definitions that are constant, or has no attribute definitions
                at all)
            BLK_XREF = This block is an external reference (xref)
            BLK_XREF_OVERLAY = This block is an xref overlay
            BLK_EXTERNAL = This block is externally dependent
            BLK_RESOLVED = This is a resolved external reference, or dependent
                of an external reference (ignored on input)
            BLK_REFERENCED = This definition is a referenced external reference
                (ignored on input)
        xref
            xref pathname (string)

        common kwargs
             linetype, color, layer, elevation?, thickness?, paper_space?,
             extrusion_direction? (see doc-string DXFEngine)
             linetype, color, layer are used by block-elements with BYBLOCK
        """
        return Block(name=name, basepoint=basepoint, **kwargs)

    @staticmethod
    def polyline(points=[], **kwargs):
        """ create a new polyline entity. Polymesh and polyface are also polylines.

        dxfwrite polylines are always 3D-polylines, 2D-polylines are not directly
        supported, but you can modify the created polylines.

        points
            list of 3D or 2D points (xy- or xyz-tuples), default z-value for 2d
            points is 0.
        see Polyline object:
            polyline.add_vertex(point)
            polyline.add_vertices( [points] )
            polyline.close(Bool)

        KWARGS

        polyline_elevation
            polyline elevation (xyz-tuple), z-axis supplies elevation, x- and
            y-axis has to be 0.)
        flags
            polyline flags, bit-coded, default=0
            POLYLINE_CLOSED = This is a closed Polyline (or a polygon mesh closed
                in the M direction)
            POLYLINE_MESH_CLOSED_M_DIRECTION = POLYLINE_CLOSED
            POLYLINE_CURVE_FIT_VERTICES_ADDED = Curve-fit vertices have been added
            POLYLINE_SPLINE_FIT_VERTICES_ADDED = Spline-fit vertices have been added
            POLYLINE_3D_POLYLINE = This is a 3D Polyline
            POLYLINE_3D_POLYMESH = This is a 3D polygon mesh
            POLYLINE_MESH_CLOSED_N_DIRECTION = The polygon mesh is closed in the
                N direction
            POLYLINE_POLYFACE_MESH = This Polyline is a polyface mesh
            POLYLINE_GENERATE_LINETYPE_PATTERN = The linetype pattern is generated
                continuously around the vertices of this Polyline
        startwidth
            default starting width (float), default=0
        endwidth
            default ending width (float), default=0
        mcount
            polygon mesh M vertex count (int), default=0
        ncount
            polygon mesh N vertex count (int), default=0
        msmooth_density (if flags-bit POLYLINE_3D_POLYMESH is set)
            smooth surface M density (int), default=0
            POLYMESH_NO_SMOOTH = no smooth surface fitted
            POLYMESH_QUADRIC_BSPLINE = quadratic B-spline surface
            POLYMESH_CUBIC_BSPLINE = cubic B-spline surface
            POLYMESH_BEZIER_SURFACE = Bezier surface
        nsmooth_density (if flags-bit POLYLINE_3D_POLYMESH is set)
            smooth surface N density, (int), default=0
            same values as msmooth_density
        smooth_surface
            curves and smooth surface type (int), default=0
            ??? see dxf-documentation

        common kwargs
             linetype, color, layer, elevation?, thickness?, paper_space,
             extrusion_direction? (see doc-string DXFEngine)
        """
        return Polyline(points, **kwargs)

    @staticmethod
    def polymesh(nrows, ncols, **kwargs):
        """ create a new polymesh entity, polymesh is a dxf-polyline entity!

        nrows and ncols >=2 and <= 256, greater meshes have to be divided into
        smaller meshes.

        flags-bit POLYLINE_3D_POLYMESH is set.
        see Polymesh object:
            polymesh.set_vertex(row, col, xyz-tuple)
            polymesh.set_mclosed()
            polymesh.set_nclosed()

        KWARGS
            see polyline
        """
        return Polymesh(nrows, ncols, **kwargs)

    @staticmethod
    def polyface(precision=6, **kwargs):
        """ create a new polyface entity, polyface is a dxf-polyline entity!

        precision
            vertex-coords will be rounded to precision places, and if the vertex
            is equal to an other vertex, only one vertex will be used, this
            reduces filespace, the coords will be rounded only for the comparison
            of the vertices, the output file has the full float resolution.

        flags-bit POLYLINE_POLYFACE is set.
        see Polyface object:
            polyface.add_face(vertices, color)
            vertices is a list of 3 or 4 xyz-tuples

        KWARGS
            see polyline
        """
        return Polyface(precision, **kwargs)

#--- Buildups

    @staticmethod
    def mtext(text, insert, linespacing=1.5, **kwargs):
        """ MultiLine-Text buildup with simple Text-Entities.

        Mostly the same kwargs like text().
        Caution: align point is always the insert point, I don't need a second
        alignpoint because horizontal alignment FIT, ALIGN, BASELINE_MIDDLE is
        not supported.

        linespacing
            linespacing in percent of height, 1.5 = 150% = 1+1/2 lines
        """
        return MText(text, insert, linespacing, **kwargs)