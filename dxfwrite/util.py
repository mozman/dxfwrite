#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: utility functions
# module belongs to package dxfwrite
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

def int2hex(value):
    return hex(value)[2:].upper()

def hex2int(string):
    return int(string, 16)

def set_flag(value, bitmask, switch_on=True):
    if switch_on:
        return value | bitmask
    else:
        return value & ~bitmask

def iterflatlist(alist):
    for element in alist:
        if hasattr(element, "__iter__") and not isinstance(element, basestring):
            for item in iterflatlist(element):
                yield item
        else:
            yield element
