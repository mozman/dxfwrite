#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: examples for dxfwrite usage, see also tests for examples
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

import sys
import os

from copy import deepcopy

try:
    import dxfwrite
except ImportError:
    # if dxfwrite is not 'installed' append parent dir of __file__ to sys.path
    import os
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

def get_mat_symbol():
    p1 = 0.5
    p2 = 0.25
    points = [(p1, p2), (p2, p1), (-p2, p1), (-p1, p2), (-p1, -p2),
              (-p2, -p1), (p2, -p1), (p1, -p2)]
    polygon = dxf.polyline(points, color=2)
    polygon.close()
    attdef = dxf.attdef(text='0', tag='num', height=0.7, color=1,
                        halign=dxfwrite.CENTER, valign=dxfwrite.MIDDLE
                        )
    symbolblock = dxf.block('matsymbol')
    symbolblock.add(polygon)
    symbolblock.add(attdef)
    dwg.blocks.add(symbolblock)
    return symbolblock

name = 'table.dxf'
dwg = dxf.drawing(name) # create a drawing
table = dxf.table(insert=(0, 0), nrows=20, ncols=10)
# create a new styles
ctext = table.new_cell_style('ctext', textcolor=7, textheight=0.5,
                             halign=dxfwrite.CENTER,
                             valign=dxfwrite.MIDDLE
                             )
# modify border settings
border = table.new_border_style(color=6, linetype='DOT', priority=51)
ctext.set_border_style(border, right=False)

table.new_cell_style('vtext', textcolor=3, textheight=0.3,
                     rotation=90, # vertical written
                     halign=dxfwrite.CENTER,
                     valign=dxfwrite.MIDDLE,
                     bgcolor=8,
                     )
# set colum width, first column has index 0
table.set_col_width(1, 7)

#set row height, first row has index 0
table.set_row_height(1, 7)

# create a text cell with the default style
cell1 = table.text_cell(0, 0, 'Zeile1\nZeile2', style='ctext')

# cell spans over 2 rows and 2 cols
cell1.span=(2, 2)

cell2 = table.text_cell(4, 0, 'VERTICAL\nTEXT', style='vtext', span=(4, 1))

# create frames
table.frame(0, 0, 10, 2, 'framestyle')

# because style is defined by a namestring
# style can be defined later
hborder = table.new_border_style(color=4)
vborder = table.new_border_style(color=17)
table.new_cell_style('framestyle', left=hborder, right=hborder,
                     top=vborder, bottom=vborder)
mat_symbol = get_mat_symbol()

table.new_cell_style('matsym',
                     halign=dxfwrite.CENTER,
                     valign=dxfwrite.MIDDLE,
                     xscale=0.6, yscale=0.6)

# add table as anonymous block
# dxf creation is only done on save, so all additional table inserts
# which will be done later, also appear in the anonymous block.

dwg.add_anonymous_block(table, insert=(40, 20))

# if you want different tables, you have to deepcopy the table
newtable = deepcopy(table)
newtable.new_cell_style('57deg', textcolor=2, textheight=0.5,
                     rotation=57, # write
                     halign=dxfwrite.CENTER,
                     valign=dxfwrite.MIDDLE,
                     bgcolor=123,
                     )
newtable.text_cell(6, 3, "line one\nline two\nand line three",
                   span=(3,3), style='57deg')
dwg.add_anonymous_block(newtable, basepoint=(0, 0), insert=(80, 20))

# a stacked text: Letters are stacked top-to-bottom, but not rotated
table.new_cell_style('stacked', textcolor=6, textheight=0.25,
                     halign=dxfwrite.CENTER,
                     valign=dxfwrite.MIDDLE,
                     stacked=True)
table.text_cell(6, 3, "STACKED FIELD", span=(7, 1), style='stacked')

for pos in [3, 4, 5, 6]:
    blockcell = table.block_cell(pos, 1, mat_symbol,
                                attribs={'num': pos},
                                style='matsym')

dwg.add(table)
dwg.save()
print("drawing '%s' created.\n" % name)
