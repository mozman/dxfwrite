#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: composite entities, consisting of basic R12 entities
# module belongs to package: dxfwrite.py
# Created: 09.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3
"""
2D Rectangle, with optional background filling
"""

import math
from dxfwrite.vector2d import *
from dxfwrite.algebra import rotate_2d

import dxfwrite.const as const
from dxfwrite.base import DXFList
from dxfwrite.entities import Polyline, Solid

class Rectangle(object):
    """ 2D Rectangle, consisting of a polyline and a solid as background filling.
    """
    name = 'RECTANGLE'

    def __init__(self, insert, width, height, rotation=0.,
                 halign=const.LEFT, valign=const.TOP,
                 color=const.BYLAYER, bgcolor=None,
                 layer='0', linetype=None):
        self.insert = insert
        self.width = float(width)
        self.height = float(height)
        self.rotation = math.radians(rotation)
        self.halign = halign
        self.valign = valign
        self.color = color
        self.bgcolor = bgcolor
        self.layer = layer
        self.linetype = linetype
        self.points = None
        self.data = DXFList()

    def _build_rect(self):
        self._calc_corners()
        if self.color is not None:
            self._build_polyline()
        if self.bgcolor is not None:
            self._build_solid()

    def _calc_corners(self):
        points = [(0., 0.), (self.width, 0.), (self.width, self.height),
                  (0., self.height)]
        align_vector = self._get_align_vector()
        self.points = [vadd(self.insert, # move to insert point
                            rotate_2d( # rotate at origin
                                vadd(point, align_vector), self.rotation))
                       for point in points]

    def _get_align_vector(self):
        if self.halign == const.CENTER:
            dx = -self.width/2.
        elif self.halign == const.RIGHT:
            dx = -self.width
        else: # const.LEFT
            dx = 0.

        if self.valign == const.MIDDLE:
            dy = -self.height/2.
        elif self.valign == const.BOTTOM:
            dy = -self.height
        else: #const.TOP
            dy = 0.

        return (dx, dy)

    def _build_polyline(self):
        """ build the rectangle with a polyline """
        polyline = Polyline(self.points, color=self.color, layer=self.layer)
        polyline.close()
        if self.linetype is not None:
            polyline['linetype'] = self.linetype
        self.data.append(polyline)

    def _build_solid(self):
        """ build the background solid """
        self.data.append(Solid(
            self.points, color=self.bgcolor, layer=self.layer))

    def __dxf__(self):
        """ get the dxf string """
        self._build_rect()
        return self.data.__dxf__()
