#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: utility functions
# module belongs to package dxfwrite
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import sys
PYTHON3 = sys.version_info[0] > 2
if PYTHON3:
    izip = zip
    unicode_seq = b'\\u'
    replace_seq = b'\\U+'

else:
    from itertools import izip
    unicode_seq = '\\u'
    replace_seq = '\\U+'

# Python 3 adaption
def is_string(value):
    if PYTHON3:
        return isinstance(value, str)
    else:
        return isinstance(value, basestring)

def to_unicode(value):
    if PYTHON3:
        return str(value)
    else:
        return str(value).decode('utf-8')

def to_string(value):
    # hook for Python 2/3 unicode problems
    if not is_string(value):
        return str(value)
    else:
        try:
            escaped_value = value.encode("raw_unicode_escape")
            assert unicode_seq in escaped_value
            escaped_value = escaped_value.replace(unicode_seq, replace_seq)
            if PYTHON3: # needs an unicode string
                return str(escaped_value, 'utf-8')
            else:
                return escaped_value
        except (UnicodeDecodeError, AssertionError):
            return value

# Python 3 adaption

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
