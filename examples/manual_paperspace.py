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
    dwg = dxf.drawing('paper_space.dxf')

    dwg.add(dxf.text('Text1 in $MODEL_SPACE'))
    dwg.add(dxf.text('Text in $PAPER_SPACE', paper_space=1))
    dwg.add(dxf.text('Text2 in $MODEL_SPACE', (0, 2)))

    dwg.save()

if __name__=='__main__':
    main()