#!/usr/bin/env python
#coding:utf-8
# Author:  raz
# Purpose: Using unicode text in the drawing
# Created: 22.11.2011
# Copyright (C) 2011, Toni Ruža, mozman
# License: GPLv3

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os, sys
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

from dxfwrite import DXFEngine as dxf

from dxfwrite.util import PYTHON3
assert PYTHON3, "This script requires Python3"

drawing = dxf.drawing('unicode_text_for_python3.dxf')
drawing.add(dxf.line((0, 0), (24, 0), color=7))

layer_name = 'ŽĆČĐŠ'
my_text = 'На крај села жута ћирилична кућа'

drawing.add_layer(layer_name, color=2)
drawing.add(dxf.text(my_text, insert=(0, 0.2), layer=layer_name))
drawing.save()
