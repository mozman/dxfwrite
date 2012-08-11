#!/usr/bin/env python
#coding:utf-8
# Purpose: The MText entity is a composite entity, consisting of basic TEXT entities.
# module belongs to package: dxfwrite
# Created: 09.03.2010
# Copyright (C) 2010, 2011, Manfred Moitzi
# License: MIT License
"""
MText -- MultiLine-Text-Entity, created by simple TEXT-Entities.

MTEXT was introduced in R13, so this is a replacement with multiple simple
TEXT entities. Supports valign (TOP, MIDDLE, BOTTOM), halign (LEFT, CENTER,
RIGHT), rotation for an arbitrary (!) angle and mirror.

"""

__author__ = "mozman <mozman@gmx.at>"

import math

import dxfwrite
from dxfwrite.base import DXFList, dxfstr
from dxfwrite.entities import Text
from dxfwrite.mixins import SubscriptAttributes

class MText(SubscriptAttributes):
    """ MultiLine-Text buildup with simple Text-Entities.

    Mostly the same kwargs like DXFEngine.text().
    Caution: align point is always the insert point, I don't need a second
    alignpoint because horizontal alignment FIT, ALIGN, BASELINE_MIDDLE is not
    supported.

    linespacing -- linespacing in percent of height, 1.5 = 150% = 1+1/2 lines
    
    """
    name = 'MTEXT'

    def __init__(self, text, insert, linespacing=1.5, **kwargs):
        self.textlines = text.split('\n')
        self.insert = insert
        self.linespacing = linespacing
        self.valign = kwargs.get('valign', dxfwrite.TOP) # only top, middle, bottom
        if self.valign == dxfwrite.BASELINE: # baseline for MText not usefull
            self.valign = dxfwrite.BOTTOM
        self.halign = kwargs.get('halign', dxfwrite.LEFT) # only left, center, right
        self.height = kwargs.get('height', 1.0)
        self.style = kwargs.get('style', 'STANDARD')
        self.oblique = kwargs.get('oblique', 0.0) # in degree
        self.rotation = kwargs.get('rotation', 0.0) # in degree
        self.xscale = kwargs.get('xscale', 1.0)
        self.mirror = kwargs.get('mirror', 0)
        self.layer = kwargs.get('layer', '0')
        self.color = kwargs.get('color', dxfwrite.BYLAYER)

    @property
    def lineheight(self):
        """ Absolute linespacing in drawing units. 
        """
        return self.height * self.linespacing
    
    def _build_dxf_entities(self):
        """ Create the DXF-TEXT entities. 
        """
        dxf_entities = DXFList()
        textlines = self.textlines
        
        if len(textlines) > 1:
            if self.mirror & dxfwrite.MIRROR_Y:
                textlines.reverse()
            for linenum, text in enumerate(textlines):
                alignpoint = self._get_align_point(linenum)
                params = self._build_text_params(alignpoint)
                dxf_entities.append(Text(text=text, **params))
        elif len(textlines) == 1:
            params = self._build_text_params(self.insert)
            dxf_entities = Text(text=textlines[0], **params).__dxftags__()
        return dxf_entities
        
    def _get_align_point(self, linenum):
        """ Calculate the align point depending on the line number. 
        """
        x = self.insert[0]
        y = self.insert[1]
        try:
            z = self.insert[2]
        except IndexError:
            z = 0.
        # rotation not respected
        if self.valign == dxfwrite.TOP:
            y -= linenum * self.lineheight
        elif self.valign == dxfwrite.MIDDLE:
            y0 = linenum * self.lineheight
            fullheight = (len(self.textlines) - 1) * self.lineheight
            y += (fullheight/2) - y0
        else: # dxfwrite.BOTTOM
            y += (len(self.textlines) - 1 - linenum) * self.lineheight
        return self._rotate( (x, y, z) ) # consider rotation

    def _rotate(self, alignpoint):
        """ Rotate alignpoint around insert point about rotation degrees. 
        """
        dx = alignpoint[0] - self.insert[0]
        dy = alignpoint[1] - self.insert[1]
        beta = math.radians(self.rotation)
        x = self.insert[0] + dx * math.cos(beta) - dy * math.sin(beta)
        y = self.insert[1] + dy * math.cos(beta) + dx * math.sin(beta)
        return (round(x, 6), round(y, 6), alignpoint[2])

    def _build_text_params(self, alignpoint):
        """ Build keyword arguments for the DXF-Text entity creation. 
        """
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
        """ Get the DXF string. 
        """
        return dxfstr(self.__dxftags__())

    def __dxftags__(self):
        return self._build_dxf_entities()
    
