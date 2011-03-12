#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: Line pattern definition
# Created: 15.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3


from dxfwrite.base import DXFList, DXFInt, DXFFloat

class LinePatternDef(DXFList):
    """
    Line pattern definition for Linetype().

    :param linedef: list of floats
       linedef[0] = total pattern length in drawing units
       linedef[n] = line segment, > 0 is line, < 0 is gap, 0.0 = dot
    """
    def __init__(self, linedef):
        count = len(linedef)-1 # the number of linetype elements
        self.append(DXFInt(65, 72)) # Alignment code; value is always 65, ASCII for 'A'
        self.append(DXFInt(count, 73)) # the number of linetype elements
        self.append(DXFFloat(linedef[0])) # total pattern length
        for element in linedef[1:]:
            self.append(DXFFloat(element, 49)) # line segment
