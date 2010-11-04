#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: 'flag' example
# Created: 04.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import random

from dxfwrite import DXFEngine as dxf

def get_random_point():
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    return (x, y)

sample_coords = [get_random_point() for x in range(50)]

flag_symbol = [(0,0), (1.294, 4.83), (3.933, 3.087), (0.776, 2.898)]

def main(filename):
    dwg = dxf.drawing(filename)
    dwg.add_layer('FLAGS')

    # first create a block
    flag = dxf.block(name='flag')
    # add dxf entities to the block (the flag)
    # use basepont = (x, y) define an other basepoint than (0 ,0)
    flag.add( dxf.polyline(flag_symbol) )
    # add block definition to the drawing
    dwg.blocks.add(flag)
    for point in sample_coords:
        # now insert flag symbols at coordinate 'point'
        # block are referenced by name, in this case: 'flag'
        # see https://bitbucket.org/mozman/dxfwrite/wiki/Insert
        # additional parameters like xscale, yscale, rotation
        #
        dwg.add(dxf.insert('flag', insert=point, layer='FLAGS'))

    dwg.save()

if __name__=='__main__':
    main("flags.dxf")