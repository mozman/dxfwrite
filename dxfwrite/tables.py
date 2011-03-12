#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: tables R12
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3


from dxfwrite.base import *

class Tables(object):
    """ Table factory. """
    @staticmethod
    def get(name):
        if name == 'VPORT':
            return Viewports()
        elif name in ['LTYPE', 'LAYER', 'STYLE', 'VIEW', 'APPID', 'UCS']:
            return _Table(name)
        else:
            raise ValueError("unknown table '%s'" % str(name))

class _Table(object):
    """ Base table class.
    """
    def __init__(self, tablename):
        self.tablename = tablename
        self._entries = {} # use only add() for adding objects

    def __dxf__(self):
        return dxfstr(
            DXFList( (
                DXFAtom('TABLE'),
                DXFName(self.tablename),
                DXFInt(len(self._entries)),
                DXFList(self._get_values()),
                DXFAtom('ENDTAB')
            )))

    def __contains__(self, name):
        return name in self._entries

    def clear(self):
        self._entries.clear()

    def _get_values(self):
        return self._entries.values()

    def add(self, entry):
        """ add ONE entry """
        self._entries[entry['name']] = entry

class Viewports(_Table):
    def __init__(self):
        super(Viewports, self).__init__('VPORT')
        # because the VPORT-table can have multiple entries with the same name
        # use a list() instead of a dict().
        self._entries = []

    def _get_values(self):
        return self._entries

    def add(self, viewport):
        self._entries.append(viewport)

    def clear(self):
        self._entries = []
