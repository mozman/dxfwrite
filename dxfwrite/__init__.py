#!/usr/bin/env python
#coding:utf-8
# Author:  mozman <mozman@gmx.at>
# Purpose: write DXF R12 files
# Based on the ideas of Stani Michiels(Stani) sdxf.py and
# Remigiusz Fiedler(migius) dxflibrary133.py
# Created: 14.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from dxfwrite.const import *
from dxfwrite.base import *
from dxfwrite.engine import DXFEngine

__version__ = "v0.3.6 - 2010.14.11"
__author__ = "Manfred Moitzi (mozman)"
__license__ = "GPLv3"

__doc__ = """A Python library to create DXF R12 drawings.

Copyright %s
Version %s
License %s

IMPLEMENTED R12 WRITING:
- POINT
- LINE
- CIRCLE
- ARC
- TEXT
- SOLID
- FACE3D
- POLYLINE (POLYMESH, POLYFACE)
- BLOCK
- INSERT
- ATTDEF
- ATTRIB

NOT IMPLEMENTED:
- TRACE
- DIMENSION (use LinearDimension, AngularDimension, ArcDimension or
             RadialDimension)
""" % (__author__,__version__,__license__,)

# --------------------------------------------------------------------------
# dxfwrite.py: copyright (C) 2010 by Manfred Moitzi (mozman)
# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
