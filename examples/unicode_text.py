#!/usr/bin/env python
#coding:utf-8
# Author:  raz
# Purpose: Using unicode text in the drawing
# Created: 22.11.2011
# Copyright (C) 2010, Toni Ruža
# License: MIT License

from __future__ import unicode_literals

__author__ = "raz"

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os, sys
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

from dxfwrite import DXFEngine as dxf

drawing = dxf.drawing('unicode_text.dxf')
drawing.add(dxf.line((0, 0), (24, 0), color=7))
layer_name = 'ŽĆČĐŠ'
drawing.add_layer(layer_name, color=2)
drawing.add(dxf.text(
    'На крај села жута ћирилична кућа', insert=(0, 0.2), layer=layer_name
))
drawing.save()
