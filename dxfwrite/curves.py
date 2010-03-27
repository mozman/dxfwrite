#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: curve objects
# Created: 26.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3
from math import sin, cos, radians

from dxfwrite.vectormath import vadd
import dxfwrite.const as const
from dxfwrite import DXFList
from dxfwrite.entities import Polyline
from dxfwrite.util import rotate_2d
from dxfwrite.algebra import CubicSpline, CubicBezierCurve
from dxfwrite.algebra import Clothoid as _ClothoidValues


class Ellipse(object):
    def __init__(self, center=(0., 0., 0.), radiusx=1.0, radiusy=1.0,
                 startangle=0., endangle=360., rotation=0., segments=100,
                 color=const.BYLAYER, layer='0', linetype=None):
        self.color = color
        self.layer = layer
        self.linetype = linetype
        self.center = center
        self.radiusx = radiusx
        self.radiusy = radiusy
        self.startangle = startangle
        self.endangle = endangle
        self.rotation = rotation
        self.segments = segments

    def _build_curve(self):
        def curve_point(alpha):
            alpha = radians(alpha)
            point = (cos(alpha) * self.radiusx,
                     sin(alpha) * self.radiusy)
            point = rotate_2d(point, self.rotation)
            x, y = vadd(self.center, point)
            return (x, y, zaxis)
        zaxis = 0. if len(self.start)<3 else self.start[2]
        points = []
        delta = (self.endangle - self.startangle) / self.segments
        for segment in xrange(self.segments):
            alpha = self.startangle + delta * segment
            points.append(curve_point(alpha))
        polyline = Polyline(points, color=self.color, layer=self.layer,
                            linetype=self.linetype)
        return polyline

    def __dxf__(self):
        self._build_curve().__dxf__()

class Bezier(object):
    class Segment(object):
        def __init__(self, start, end, start_tangent, end_tangent, segments):
            self.start = start
            self.end = end
            self.start_tangent = start_tangent # as 2d vector, from start point
            self.end_tangent = end_tangent # as 2d vector, from end point
            self.segments = segments

        def approximate(self):
            control_points = [
                self.start,
                vadd(self.start, self.start_tangent),
                vadd(self.end, self.end_tangent),
                self.end ]
            bezier = CubicBezierCurve(control_points)
            bezier_points = []
            delta = 1. / self.segments
            for param in xrange(self.segments+1): # [0 .. 1]
                bezier_points.append(bezier.get_point(param * delta))
            return Polyline(bezier_points)

    def __init__(self, color=const.BYLAYER, layer='0', linetype=None):
        self.color = color
        self.layer = layer
        self.linetype = linetype
        self.points = []

    def start_point(self, point, tangent):
        """Defines the start point and the start tangent.

        point -- 2D start point
        tangent -- start tangent as 2D vector, example: (5, 0) means a horizontal
            tangent with a length of 5 drawing units
        """
        self.points.append( (point, None, tangent, None) )

    def append_point(self, point, tangent1, tangent2=None, segments=20):
        """Append a control point with two control tangents.

        point -- the control point as 2D point
        tangent1 -- first control tangent as 2D vector 'left' of point
        tangent2 -- second control tangent as 2D vector 'right' of point, if
            omitted tangent2 = -tangent1
        segments -- count of points to use for polyline approximation, count of
            points from previous control point to this point.
        """
        if tangent2 is None:
            tangent2 = (-tangent1[0], -tangent1[1])
        self.points.append( (point, tangent1, tangent2, segments) )

    def _build_bezier_segments(self):
        if len(self.points)>1:
            for from_point, to_point in zip(self.points[:-1], self.points[1:]):
                start_point = from_point[0]
                start_tangent = from_point[3] # tangent2
                end_point = to_point[0]
                end_tangent = to_point[1] # tangent1
                count = to_point[3]
                yield Bezier.Segment(start_point, end_point,
                                     start_tangent, end_tangent, count)
        else:
            raise ValueError('Tow or more points needed!')

    def _build_curve(self):
        polylines = DXFList()
        for segment in self._build_bezier_segments():
            polyline = segment.approximate()
            polyline['layer'] = self.layer
            polyline['color'] = self.color
            polyline['linetyle'] = self.linetype
            polylines.append(polyline)
        return polylines

    def __dxf__(self):
        self._build_curve().__dxf__()

class Spline(object):
    def __init__(self, points=[], segments=100, color=const.BYLAYER, layer='0',
                 linetype=None):
        self.color = color
        self.layer = layer
        self.linetype = linetype
        self.points = points
        self.segments = segments

    def _build_curve(self):
        spline = CubicSpline(self.points)
        polyline = Polyline(spline.approximate(self.segments),
                            layer = self.layer,
                            color=self.color,
                            linetype = self.linetype)
        return polyline

    def __dxf__(self):
        self._build_curve().__dxf__()

class Clothoid(object):
    def __init__(self, start=(0, 0), start_tangent=0., length=1., paramA=1.0,
                 mirrorx=False, mirrory=False, segments=100,
                 color=const.BYLAYER, layer='0', linetype=None):
        self.color = color
        self.layer = layer
        self.linetype = linetype
        self.start = start
        self.start_tangent = start_tangent
        self.length = length
        self.paramA = paramA
        self.mirrorx = mirrorx
        self.mirrory = mirrory
        self.segments = segments

    def _build_curve(self):
        def cpoint(distance):
            point = clothoid.get_xy(distance)
            if self.mirrorx:
                point[1] = -point[1]
            if self.mirrory:
                point[0] = -point[0]
            point = rotate_2d(point, rotation)
            x, y = vadd(self.start, point)
            return (x, y, zaxis)

        zaxis = 0. if len(self.start)<3 else self.start[2]
        rotation = radians(self.start_tangent)
        clothoid = _ClothoidValues(self.paramA)
        points = []
        seg_length = self.length / self.segments
        for segment in xrange(self.segments+1):
            self.points.append(cpoint(seg_length * segment))
        return Polyline(points, color=self.color, layer=self.layer,
                        linetype=self.linetype)

    def __dxf__(self):
        self._build_curve().__dxf__()
