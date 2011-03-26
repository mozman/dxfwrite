#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: try paperspace
# Created: 26.03.2011
# Copyright (C) , Manfred Moitzi
# License: GPLv3

import dxfwrite
from dxfwrite import DXFEngine as dxf

def main():
    dwg = dxf.drawing('paperspace.dxf')
    # IMPORTANT: DXF R12 supports only 1 paperspace

    # adding entities to dwg.modelspace forces the 'paper_space' attribute to be 0
    dwg.modelspace.add(dxf.text('Text1 in modelspace'))
    # adding entities to dwg.paperspace forces the 'paper_space' attribute to be 1
    dwg.paperspace.add(dxf.text('Text in paperspace'))
    # adding entities with dwg.add doen't change the 'paper_space' attribute,
    # which is 0 by default == modelspace
    dwg.add(dxf.text('Text2 also in modelspace', (0, 2)))
    dwg.add(dxf.text('Text2 also in paperspace', (0, 2), paper_space=1))

    dwg.save()

if __name__=='__main__':
    main()