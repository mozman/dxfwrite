#!/usr/bin/env python
# coding:utf-8
# Purpose: simple with basic dxf eintities created dimension lines, but not
# the basic DXF-DIMENSION entities.
# module belongs to package: dxfwrite.py
# Created: 10.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

""" Simple 2D dimension lines build with basic dxf entities, but not the basic
dxf dimension-entity!

OBJECTS

- LinearDimension
- AngularDimension
- ArcDimension
- RadialDimension

PUBLIC MEMBERS

dimstyles
    dimstyle container

    - new(name, kwargs) to create a new dimstyle
    - get(name) to get a dimstyle, 'Default' if name does not exist
    - setup(drawing) create Blocks and Layers in drawing
"""

__author__ = "mozman <mozman@gmx.at>"

from math import radians, degrees, pi

from .vector2d import *
from . import DXFList, dxfstr
from .algebra import Ray2D
from .entities import Line, Text, Block, Insert, Solid, Arc, Circle
from . import const
from .util import to_unicode

__all__ = ['LinearDimension', 'AngularDimension', 'ArcDimension',
           'RadialDimension', 'dimstyles']

DIMENSIONS_MIN_DISTANCE = 0.05
DIMENSIONS_FLOATINGPOINT = '.'

ANGLE_DEG = 180. / pi
ANGLE_GRAD = 200. / pi
ANGLE_RAD = 1.


class _DimStyle(dict):
    """ _DimStyle parameter struct, a dumb object just to store values """
    default_values = [
        # tick block name, use setup to generate default blocks
        ('tick', 'DIMTICK_ARCH'),
        # scale factor for ticks-block
        ('tickfactor', 1.),
        # tick2x means tick is drawn only for one side, insert tick a second
        # time rotated about 180 degree, but only one time at the dimension line
        # ends, this is useful for arrow-like ticks. hint: set dimlineext to 0.
        ('tick2x', False),
        # dimension value scale factor, value = drawing-units * scale
        ('scale', 100.),
        # round dimension value to roundval fractional digits
        ('roundval', 0),
        # round dimension value to half units, round 0.4, 0.6 to 0.5
        ('roundhalf', False),
        # dimension value text color
        ('textcolor', 7),
        # dimension value text height
        ('height', .5),
        # dimension text prefix and suffix like 'x=' ... ' cm'
        ('prefix', ''),
        ('suffix', ''),
        # dimension value text style
        ('style', 'ISOCPEUR'),
        # default layer for whole dimension object
        ('layer', 'DIMENSIONS'),
        # dimension line color index (0 from layer)
        ('dimlinecolor', 7),
        # dimension line extensions (in dimline direction, left and right)
        ('dimlineext', .3),
        # draw dimension value text <textabove> drawing-units above the
        # dimension line
        ('textabove', 0.2),
        # switch extension line False=off, True=on
        ('dimextline', True),
        # dimension extension line color index (0 from layer)
        ('dimextlinecolor', 5),
        # gap between measure target point and end of extension line
        ('dimextlinegap', 0.3)
    ]

    def __init__(self, name, **kwargs):
        super(_DimStyle, self).__init__(_DimStyle.default_values)
        # dimestyle name
        self['name'] = name
        self.update(kwargs)

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


class _DimStyles(object):
    """ DimStyle container
    """

    def __init__(self):
        self._styles = {}
        self.default = _DimStyle('Default')

        self.new("angle.deg", scale=ANGLE_DEG, suffix=to_unicode('°'), roundval=0,
                 tick="DIMTICK_RADIUS", tick2x=True, dimlineext=0.,
                 dimextline=False)
        self.new("angle.grad", scale=ANGLE_GRAD, suffix='gon', roundval=0,
                 tick="DIMTICK_RADIUS", tick2x=True, dimlineext=0.,
                 dimextline=False)
        self.new("angle.rad", scale=ANGLE_RAD, suffix='rad', roundval=3,
                 tick="DIMTICK_RADIUS", tick2x=True, dimlineext=0.,
                 dimextline=False)

    def get(self, name):
        """ Get DimStyle() object by name.
        """
        return self._styles.get(name, self.default)

    def new(self, name, **kwargs):
        """ Create a new dimstyle
        """
        style = _DimStyle(name, **kwargs)
        self._styles[name] = style
        return style

    @staticmethod
    def setup(drawing):
        """ Insert necessary definitions into drawing:

        - ticks: DIMTICK_ARCH, DIMTICK_DOT, DIMTICK_ARROW
        - layers: DIMENSIONS
        """
        # default pen assignment:
        # 1 : 1.40mm - red
        # 2 : 0.35mm - yellow
        # 3 : 0.70mm - green
        # 4 : 0.50mm - cyan
        # 5 : 0.13mm - blue
        # 6 : 1.00mm - magenta
        # 7 : 0.25mm - white/black
        # 8, 9 : 2.00mm
        # >=10 : 1.40mm
        def block(name, elements):
            """ Create the block entity """
            tick = Block(name=name, basepoint=(0., 0.))
            for element in elements:
                tick.add(element)
            return tick

        dimcolor = dimstyles.default.dimextlinecolor
        byblock = const.BYBLOCK

        elements = [
            Line(start=(0., +.5), end=(0., -.5), color=dimcolor,
                 layer=byblock),
            Line(start=(-.2, -.2), end=(.2, +.2), color=4, layer=byblock)
        ]
        drawing.blocks.add(block('DIMTICK_ARCH', elements))

        elements = [
            Line(start=(0., .5), end=(0., -.5), color=dimcolor, layer=byblock),
            Circle(radius=.1, color=4, layer=byblock)
        ]
        drawing.blocks.add(block('DIMTICK_DOT', elements))

        elements = [
            Line(start=(0., .5), end=(0., -.50), color=dimcolor, layer=byblock),
            Solid([(0, 0), (.3, .05), (.3, -.05)], color=7, layer=byblock)
        ]
        drawing.blocks.add(block('DIMTICK_ARROW', elements))
        elements = [  # special tick for RadialDimension
                      Solid([(0, 0), (.3, .05), (0.25, 0.), (.3, -.05)], color=7, layer=byblock)
        ]
        drawing.blocks.add(block('DIMTICK_RADIUS', elements))


dimstyles = _DimStyles()  # use this factory tu create new dimstyles


class _DimensionBase(object):
    """ Abstract base class for dimension lines.
    """

    def __init__(self, dimstyle, layer, roundval):
        self.dimstyle = dimstyles.get(dimstyle)
        self.layer = layer
        self.roundval = roundval
        self.data = DXFList()

    def prop(self, property_name):
        """ Get dimension line properties by `property_name` with the
        possibility to override several properties.
        """
        if property_name == 'layer':
            return self.layer if self.layer is not None else self.dimstyle.layer
        elif property_name == 'roundval':
            return self.roundval if self.roundval is not None else self.dimstyle.roundval
        else:  # pass through self.dimstyle object DimStyle()
            return self.dimstyle[property_name]

    def format_dimtext(self, dimvalue):
        """ Format the dimension text.
        """
        ## TODO: concider roundhalf property
        dimtextfmt = "%." + str(self.prop('roundval')) + "f"
        dimtext = dimtextfmt % dimvalue
        if DIMENSIONS_FLOATINGPOINT in dimtext:
            # remove successional zeros
            dimtext.rstrip('0')
            # remove floating point as last char
            dimtext.rstrip(DIMENSIONS_FLOATINGPOINT)
        return self.prop('prefix') + dimtext + self.prop('suffix')

    def __dxf__(self):
        """ Get the dxf string.
        """
        return dxfstr(self.__dxftags__())

    def __dxftags__(self):
        """ Get dxf tags as cascading DXFList.
        """
        self._build_dimline()
        return self.data


class LinearDimension(_DimensionBase):
    """ Simple straight dimension line with two or more measure points, build
    with basic DXF entities. This is NOT a dxf dimension entity. And This is
    a 2D element, so all z-values will be ignored!
    """

    def __init__(self, pos, measure_points, angle=0., dimstyle='Default',
                 layer=None, roundval=None):
        """ LinearDimension Constructor.

        :param pos: location as (x, y) tuple of dimension line, line goes through this point
        :param measure_points: list of points as (x, y) tuples to dimension (two or more)
        :param float angle: angle (in degree) of dimension line
        :param str dimstyle: dimstyle name, 'Default' - style is the default value
        :param str layer: dimension line layer, override the default value of dimstyle
        :param int roundval: count of decimal places
        """
        super(LinearDimension, self).__init__(dimstyle, layer, roundval)
        self.angle = angle
        self.measure_points = measure_points
        self.text_override = [""] * self.section_count
        self.dimlinepos = vector2d(pos)

    def set_text(self, section, text):
        """ Set and override the text of the dimension text for the given
        dimension line section.
        """
        self.text_override[section] = text

    def _setup(self):
        """ calc setup values and determines the point order of the dimension
        line points.
        """
        self.measure_points = [vector2d(point)
                               for point in self.measure_points]

        dimlineray = Ray2D(self.dimlinepos, angle=radians(self.angle))
        self.dimline_points = [self._get_point_on_dimline(point, dimlineray)
                               for point in self.measure_points]
        self.point_order = self._indices_of_sorted_points(self.dimline_points)
        self._build_vectors()

    def _get_dimline_point(self, index):
        """ get point on the dimension line, index runs left to right
        """
        return self.dimline_points[self.point_order[index]]

    def _get_section_points(self, section):
        """ get start and end point on the dimension line of dimension section
        """
        return (self._get_dimline_point(section),
                self._get_dimline_point(section + 1))

    def _get_dimline_bounds(self):
        """ get the first and the last point of dimension line """
        return (self._get_dimline_point(0),
                self._get_dimline_point(-1))

    @property
    def section_count(self):
        """ count of dimline sections """
        return len(self.measure_points) - 1

    @property
    def point_count(self):
        """ count of dimline points """
        return len(self.measure_points)

    def _build_dimline(self):
        """ build dimension line object with basic dxf entities """
        self._setup()
        self._draw_dimline()
        if self.prop('dimextline'):
            self._draw_extension_lines()
        self._draw_text()
        self._draw_ticks()

    @staticmethod
    def _indices_of_sorted_points(points):
        """ get indices of points, for points sorted by x, y values """
        indexed_points = [(point, idx) for idx, point in enumerate(points)]
        indexed_points.sort()
        return [idx for point, idx in indexed_points]

    def _build_vectors(self):
        """ build unit vectors, parallel and normal to dimension line """
        point1, point2 = self._get_dimline_bounds()
        self.parallel_vector = unit_vector(vsub(point2, point1))
        self.normal_vector = normal_vector(self.parallel_vector)

    @staticmethod
    def _get_point_on_dimline(point, dimray):
        """ get the measure target point projection on the dimension line """
        return dimray.intersect(dimray.normal_through(point))

    def _draw_dimline(self):
        """ build dimension line entity """
        start_point, end_point = self._get_dimline_bounds()

        dimlineext = self.prop('dimlineext')
        if dimlineext > 0:
            start_point = vsub(start_point,
                               vmul_scalar(self.parallel_vector, dimlineext))
            end_point = vadd(end_point,
                             vmul_scalar(self.parallel_vector, dimlineext))

        self.data.append(Line(
            start=start_point, end=end_point,
            color=self.prop('dimlinecolor'),
            layer=self.prop('layer')))

    def _draw_extension_lines(self):
        """ build the extension lines entities """
        dimextlinegap = self.prop('dimextlinegap')
        for dimline_point, target_point in \
                zip(self.dimline_points, self.measure_points):
            if distance(dimline_point, target_point) > \
                    max(dimextlinegap, DIMENSIONS_MIN_DISTANCE):
                direction_vector = unit_vector(vsub(target_point,
                                                    dimline_point))
                target_point = vsub(target_point, vmul_scalar(direction_vector,
                                                              dimextlinegap))
                self.data.append(Line(
                    start=dimline_point,
                    end=target_point,
                    color=self.prop('dimextlinecolor'),
                    layer=self.prop('layer')))

    def _draw_text(self):
        """ build the dimension value text entity """
        for section in range(self.section_count):
            dimvalue_text = self._get_dimvalue_text(section)
            insert_point = self._get_text_insert_point(section)
            self.data.append(Text(
                text=dimvalue_text,
                insert=insert_point,
                height=self.prop('height'),
                color=self.prop('textcolor'),
                halign=const.CENTER,
                valign=const.MIDDLE,
                layer=self.prop('layer'),
                rotation=self.angle,
                style=self.prop('style'),
                alignpoint=insert_point))

    def _get_dimvalue_text(self, section):
        """ get the dimension value as text, distance from point1 to point2 """
        override = self.text_override[section]
        if len(override):
            return override
        point1, point2 = self._get_section_points(section)

        dimvalue = distance(point1, point2) * self.prop('scale')
        return self.format_dimtext(dimvalue)

    def _get_text_insert_point(self, section):
        """ get the dimension value text insert point """
        point1, point2 = self._get_section_points(section)
        dist = self.prop('height') / 2. + self.prop('textabove')
        return vadd(midpoint(point1, point2),
                    vmul_scalar(self.normal_vector, dist))

    def _draw_ticks(self):
        """ insert the dimension line ticks, (markers on the dimension line) """

        def tick(point, rotate=False):
            """ build the insert-entity for the tick block """
            return Insert(
                insert=point,
                blockname=self.prop('tick'),
                rotation=self.angle + (180. if rotate else 0.),
                xscale=self.prop('tickfactor'),
                yscale=self.prop('tickfactor'),
                layer=self.prop('layer'))

        def set_tick(index, rotate=False):
            """ add tick to dxf data """
            self.data.append(tick(self._get_dimline_point(index), rotate))

        if self.prop('tick2x'):
            for index in range(0, self.point_count - 1):
                set_tick((index), False)
            for index in range(1, self.point_count):
                set_tick((index), True)
        else:
            for index in range(self.point_count):
                set_tick((index), False)


class AngularDimension(_DimensionBase):
    """ Draw an angle dimensioning line at dimline pos from start to end,
    dimension text is the angle build of the three points start-center-end.
    """
    DEG = ANGLE_DEG
    GRAD = ANGLE_GRAD
    RAD = ANGLE_RAD

    def __init__(self, pos, center, start, end,
                 dimstyle='angle.deg', layer=None, roundval=None):
        """ AngularDimension constructor.

        :param pos: location as (x, y) tuple of dimension line, line goes through this point
        :param center: center point as (x, y) tuple of angle
        :param start: line from center to start is the first side of the
            angle
        :param end: line from center to end is the second side of the angle
        :param str dimstyle: dimstyle name, 'Default' - style is the
            default value
        :param str layer: dimension line layer, override the default value
            of dimstyle
        :param int roundval: count of decimal places
        """
        super(AngularDimension, self).__init__(dimstyle, layer, roundval)
        self.dimlinepos = vector2d(pos)
        self.center = vector2d(center)
        self.start = vector2d(start)
        self.end = vector2d(end)

    def _setup(self):
        """ setup calculation values """
        self.pos_radius = distance(self.center, self.dimlinepos)
        self.radius = distance(self.center, self.start)
        self.start_vector = unit_vector(vsub(self.start, self.center))
        self.end_vector = unit_vector(vsub(self.end, self.center))
        self.start_angle = vector2angle(self.start_vector)
        self.end_angle = vector2angle(self.end_vector)

    def _build_dimline(self):
        """ build dimension line object with basic dxf entities """
        self._setup()
        self._draw_dimension_line()
        if self.prop('dimextline'):
            self._draw_extension_lines()
        self._draw_dimension_text()
        self._draw_ticks()

    def _draw_dimension_line(self):
        """ draw the dimension line from start- to endangle. """
        self.data.append(Arc(
            radius=self.pos_radius,
            center=self.center,
            startangle=degrees(self.start_angle),
            endangle=degrees(self.end_angle),
            layer=self.prop('layer'),
            color=self.prop('dimlinecolor')))

    def _draw_extension_lines(self):
        """ build the extension lines entities """
        for vector in [self.start_vector, self.end_vector]:
            self.data.append(
                Line(start=self._get_extline_start(vector),
                     end=self._get_extline_end(vector),
                     layer=self.prop('layer'),
                     color=self.prop('dimextlinecolor')))

    def _get_extline_start(self, vector):
        return vadd(self.center,
                    vmul_scalar(vector, self.prop('dimextlinegap')))

    def _get_extline_end(self, vector):
        return vadd(self.center, vmul_scalar(vector, self.pos_radius))

    def _draw_dimension_text(self):
        dimtext = self._get_dimtext()
        insert_point = self._get_text_insert_point()
        rotation = degrees((self.start_angle + self.end_angle) / 2 - pi / 2.)
        self.data.append(Text(
            text=dimtext,
            insert=insert_point,
            height=self.prop('height'),
            rotation=rotation,
            halign=const.CENTER,
            valign=const.MIDDLE,
            layer=self.prop('layer'),
            style=self.prop('style'),
            color=self.prop('textcolor'),
            alignpoint=insert_point))

    def _get_text_insert_point(self):
        midvector = unit_vector(
            vdiv_scalar(vadd(self.start_vector, self.end_vector), 2.))
        length = self.pos_radius + self.prop('textabove') + self.prop('height') / 2.
        return vadd(self.center, vmul_scalar(midvector, length))

    def _draw_ticks(self):
        for vector, mirror in [(self.start_vector, False),
                               (self.end_vector, self.prop('tick2x'))]:
            insert_point = vadd(self.center, vmul_scalar(
                vector, self.pos_radius))
            rotation = vector2angle(vector) + pi / 2.
            rotation = degrees(rotation + (pi if mirror else 0.))
            self.data.append(Insert(
                insert=insert_point,
                blockname=self.prop('tick'),
                rotation=rotation,
                xscale=self.prop('tickfactor'),
                yscale=self.prop('tickfactor'),
                layer=self.prop('layer')))

    def _get_dimtext(self):
        # set scale = ANGLE_DEG for degrees (circle = 360 deg)
        # set scale = ANGLE_GRAD for grad(circle = 400 grad)
        # set scale = ANGLE_RAD for rad(circle = 2*pi)
        angle = (self.end_angle - self.start_angle) * self.prop('scale')
        return self.format_dimtext(angle)


class ArcDimension(AngularDimension):
    """ Arc is defined by start- and endpoint on arc and the centerpoint, or
    by three points lying on the arc if acr3points is True. Measured length goes
    from start- to endpoint. The dimension line goes through the dimlinepos.
    """

    def __init__(self, pos, center, start, end, arc3points=False,
                 dimstyle='Default', layer=None, roundval=None):
        """
        :param pos: location as (x, y) tuple of dimension line, line goes through this point
        :param center: center point of arc
        :param start: start point of arc
        :param end: end point of arc
        :param bool arc3points: if **True** arc is defined by three points
            on the arc (center, start, end)
        :param str dimstyle: dimstyle name, 'Default' - style is the
            default value
        :param str layer: dimension line layer, override the default value
            of dimstyle
        :param int roundval: count of decimal places
        """
        super(ArcDimension, self).__init__(pos, center, start, end,
                                           dimstyle, layer, roundval)
        self.arc3points = arc3points

    def _setup(self):
        super(ArcDimension, self)._setup()
        if self.arc3points:
            self.center = center_of_3points_arc(
                self.center, self.start, self.end)

    def _get_extline_start(self, vector):
        return vadd(self.center,
                    vmul_scalar(
                        vector, self.radius + self.prop('dimextlinegap')))

    def _get_extline_end(self, vector):
        return vadd(self.center, vmul_scalar(vector, self.pos_radius))

    def _get_dimtext(self):
        arc_length = (self.end_angle - self.start_angle) * \
                     self.radius * self.prop('scale')
        return self.format_dimtext(arc_length)


class RadialDimension(_DimensionBase):
    """ Draw a radius dimension line from `target` in direction of `center` with
    length drawing units. RadialDimension has a special tick!!
    """

    def __init__(self, center, target, length=1.,
                 dimstyle='Default', layer=None, roundval=None):
        """
        :param center: center point of radius
        :param target: target point of radius
        :param float length: length of radius arrow (drawing length)
        :param str dimstyle: dimstyle name, 'Default' - style is the
            default value
        :param str layer: dimension line layer, override the default value
            of dimstyle
        :param roundval: count of decimal places
        """
        super(RadialDimension, self).__init__(dimstyle, layer, roundval)
        self.center = vector2d(center)
        self.target = vector2d(target)
        self.length = float(length)

    def _setup(self):
        self.target_vector = unit_vector(vsub(self.target, self.center))
        self.radius = distance(self.center, self.target)

    def _build_dimline(self):
        """ build dimension line object with basic dxf entities """
        self._setup()
        self._draw_dimension_line()
        self._draw_dimension_text()
        self._draw_ticks()

    def _draw_dimension_line(self):
        start_point = vadd(self.center, vmul_scalar(
            self.target_vector, self.radius - self.length))
        self.data.append(Line(
            start=start_point, end=self.target,
            layer=self.prop('layer'),
            color=self.prop('dimlinecolor')))

    def _draw_dimension_text(self):
        insert_point = self._get_insert_point()
        dimtext = self._get_dimtext()
        rotation = degrees(vector2angle(self.target_vector))
        self.data.append(Text(
            text=dimtext,
            insert=insert_point,
            height=self.prop('height'),
            rotation=rotation,
            valign=const.MIDDLE,
            halign=const.RIGHT,
            alignpoint=insert_point,
            layer=self.prop('layer'),
            style=self.prop('style'),
            color=self.prop('textcolor')))

    def _get_insert_point(self):
        return vsub(self.target, vmul_scalar(
            self.target_vector, self.length + self.prop('textabove')))

    def _get_dimtext(self):
        return self.format_dimtext(self.radius * self.prop('scale'))

    def _draw_ticks(self):
        rotation = vector2angle(self.target_vector)
        rotation = degrees(rotation + pi)
        self.data.append(Insert(
            insert=self.target,
            blockname='DIMTICK_RADIUS',
            rotation=rotation,
            xscale=self.prop('tickfactor'),
            yscale=self.prop('tickfactor'),
            layer=self.prop('layer')))


def center_of_3points_arc(point1, point2, point3):
    """ calc center point of 3 point arc

    Circle is defined by the points point1, point2 and point3.
    """
    ray1 = Ray2D(point1, point2)
    ray2 = Ray2D(point1, point3)
    midpoint1 = midpoint(point1, point2)
    midpoint2 = midpoint(point1, point3)
    center_ray1 = ray1.normal_through(midpoint1)
    center_ray2 = ray2.normal_through(midpoint2)
    return center_ray1.intersect(center_ray2)
