#!/usr/bin/env python
#coding:utf-8
# Author:   mozman
# Created: 27.03.2010
# Purpose: 3d vectormath
# module belongs to package dxfwrite
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

def vector3d(vector):
    """ return a 3d vector """
    if len(vector) == 2:
        return (float(vector[0]), float(vector[1]), 0.)
    else:
        return (float(vector[0]), float(vector[1]), float(vector[2]))
