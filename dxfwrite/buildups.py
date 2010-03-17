#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: buildups, consisting of basic R12 entities
# module belongs to package: dxfwrite.py
# Created: 09.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

""" Additional DXF-Entities buildup with basic DXF R12 Entities.

MText()
    MTEXT was introduced in R13, so this is a replacement with multiple simple
    TEXT entities. Supports valign (TOP, MIDDLE, BOTTOM), halign (LEFT, CENTER,
    RIGHT), rotation for an arbitrary (!) angle and mirror.

Rectangle()
    2D Rectangle, with optional background filling
"""

import math
from dxfwrite.vectormath import *
from dxfwrite.util import rotate_2d

import dxfwrite.const as const
from dxfwrite.base import DXFList
from dxfwrite.entities import Text, Polyline, Solid

class MText(object):
    """ MultiLine-Text buildup with simple Text-Entities.

    Mostly the same kwargs like DXFEngine.text().
    Caution: align point is always the insert point, I don't need a second
    alignpoint because horizontal alignment FIT, ALIGN, BASELINE_MIDDLE is not
    supported.

    linespacing
        linespacing in percent of height, 1.5 = 150% = 1+1/2 lines
    """
    def __init__(self, text, insert, linespacing=1.5, **kwargs):
        self.textlines = text.split('\n')
        self.insert = insert
        self.linespacing = linespacing
        self.valign = kwargs.get('valign', const.TOP) # only top, middle, bottom
        if self.valign == const.BASELINE: # baseline for MText not usefull
            self.valign = const.BOTTOM
        self.halign = kwargs.get('halign', const.LEFT) # only left, center, right
        self.height = kwargs.get('height', 1.0)
        self.style = kwargs.get('style', 'STANDARD')
        self.oblique = kwargs.get('oblique', 0.0) # in degree
        self.rotation = kwargs.get('rotation', 0.0) # in degree
        self.xscale = kwargs.get('xscale', 1.0)
        self.mirror = kwargs.get('mirror', 0)
        self.layer = kwargs.get('layer', '0')
        self.color = kwargs.get('color', const.BYLAYER)
        self.data = DXFList()

        if len(self.textlines)>1: # more than one line
            self._build_dxf_text_entities()
        elif len(self.textlines) == 1: # just a normal text with one line
            kwargs['alignpoint'] = insert # text() needs the align point
            self.data.append(Text(text=text, insert=insert, **kwargs))

    @property
    def lineheight(self):
        """ absolute linespacing in drawing units """
        return self.height * self.linespacing

    def _build_dxf_text_entities(self):
        """ create the dxf TEXT entities """
        if self.mirror & const.MIRROR_Y:
            self.textlines.reverse()
        for linenum, text in enumerate(self.textlines):
            alignpoint = self._get_align_point(linenum)
            params = self._build_text_params(alignpoint)
            self.data.append(Text(text=text, **params))

    def _get_align_point(self, linenum):
        """ calculate the align point depending on the line number. """
        x = self.insert[0]
        y = self.insert[1]
        try:
            z = self.insert[2]
        except IndexError:
            z = 0.
        # rotation not respected
        if self.valign == const.TOP:
            y -= linenum * self.lineheight
        elif self.valign == const.MIDDLE:
            y0 = linenum * self.lineheight
            fullheight = (len(self.textlines) - 1) * self.lineheight
            y += (fullheight/2) - y0
        else: # const.BOTTOM
            y += (len(self.textlines) - 1 - linenum) * self.lineheight
        return self._rotate( (x, y, z) ) # consider rotation

    def _rotate(self, alignpoint):
        """ rotate alignpoint around insert point about rotation degrees """
        dx = alignpoint[0] - self.insert[0]
        dy = alignpoint[1] - self.insert[1]
        beta = math.radians(self.rotation)
        x = self.insert[0] + dx * math.cos(beta) - dy * math.sin(beta)
        y = self.insert[1] + dy * math.cos(beta) + dx * math.sin(beta)
        return (round(x, 6), round(y, 6), alignpoint[2])

    def _build_text_params(self, alignpoint):
        """ build the calling dict for Text() """
        return {
            'insert': alignpoint,
            'alignpoint': alignpoint,
            'layer': self.layer,
            'color': self.color,
            'style': self.style,
            'height': self.height,
            'xscale': self.xscale,
            'mirror': self.mirror,
            'rotation': self.rotation,
            'oblique': self.oblique,
            'halign': self.halign,
            'valign': self.valign,
        }

    def __dxf__(self):
        """ get the dxf string """
        return self.data.__dxf__()

class Rectangle(object):
    """ 2D Rectangle, build with a polyline an d a solid as background filling

    insert point

    width, height
        in drawing units

    rotation
        in degree

    halign
        LEFT, CENTER, RIGHT

    valign
        TOP, MIDDLE, BOTTOM

    color
        dxf color index, default is BYLAYER, if color is None, no polyline
        will be created, and the rectangle consist only of the background
        filling (if bgcolor != None)

    bgcolor
        dxf color index, default is None (no background filling)

    layer
        target layer, default is '0'

    linetype
        linetype name, None = BYLAYER
    """
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
