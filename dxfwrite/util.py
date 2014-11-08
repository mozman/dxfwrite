#!/usr/bin/env python
# coding:utf-8
# Purpose: utility functions
# module belongs to package dxfwrite
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import sys
PYTHON3 = sys.version_info[0] > 2

if PYTHON3:
    from io import StringIO
    izip = zip

    def is_string(value):
        return isinstance(value, str)

    def to_unicode(value):
        return str(value)

    def to_string(value):
        if not isinstance(value, str):
            return str(value)
        else:
            escaped_value = value.encode("raw_unicode_escape")
            if b'\\u' in escaped_value:
                return str(escaped_value.replace(b'\\u', b'\\U+'), 'utf-8')
            else:
                return value
else:  # PYTHON2
    from itertools import izip
    from StringIO import StringIO

    def is_string(value):
        return isinstance(value, basestring)

    def to_unicode(value):
        return str(value).decode('utf-8')

    def to_string(value):
        if not isinstance(value, basestring):
            return str(value)
        else:
            escaped_value = value.encode("raw_unicode_escape")
            if '\\u' in escaped_value:
                return escaped_value.replace('\\u', '\\U+')
            else:
                return value

# end of Python 2/3 adaption


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
        if hasattr(element, "__iter__") and not is_string(element):
            for item in iterflatlist(element):
                yield item
        else:
            yield element
