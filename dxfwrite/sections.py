#coding:utf-8
# Author:  mozman
# Purpose: sections R12
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3


__all__ = ['Sections']

from dxfwrite.base import DXFAtom, DXFList, DXFName, dxfstr
from dxfwrite.tables import Tables

class Sections(object):
    @staticmethod
    def get(name):
        if name == 'HEADER':
            return Header()
        elif name == 'BLOCKS':
            return Blocks()
        elif name == 'ENTITIES':
            return Entities()
        elif name == 'TABLES':
            return TablesSection()
        else:
            raise ValueError("unknown section '%s'" % str(name))

class _Section(object):
    def __dxf__(self):
        head = dxfstr(DXFAtom('SECTION'))
        body = dxfstr(self._get_body())
        tail = dxfstr(DXFAtom('ENDSEC'))
        return "".join( (head, body, tail) )

    def _get_body(self):
        return DXFList()

class Header(_Section):
    def __init__(self, default_vars=None):
        self.variables = {}
        if default_vars:
            self.add_vars(default_vars)

    def _get_body(self):
        """ Return header section content as DXFList.
        """
        varlist = [DXFList((DXFAtom(key, 9), value))
                   for key, value in self.variables.items()]
        return DXFList( (DXFName('HEADER'),
                          DXFList(varlist)
                          ) )

    def get(self, varname):
        return self.variables[varname]

    def add(self, name, value):
        """ Set header variable <name> to <value>.

        Arguments
        ---------
        name -- variable name
        value -- dxfwrite.base.DXFAtom() or inherited

        usage:
            add('$ACADVER', DXFString('AC1018'))
        """
        self.variables[name] = value

    def add_vars(self, variables):
        """Add many vars to header.

        Arguments
        ---------
        variables -- list of tuples ('varname', dxfwrite.base.DXFAtom())

        usage:
            add_vars([('$ACADVER', DXFString('AC1018')), ('$EXTMIN', DXFPoint())])
        """
        for name, value in variables:
            self.add(name, value)


class TablesSection(_Section):
    def __init__(self):
        self.linetypes = Tables.get('LTYPE')
        self.layers = Tables.get('LAYER')
        self.styles = Tables.get('STYLE')
        self.views = Tables.get('VIEW')
        self.viewports = Tables.get('VPORT')
        self.appids = Tables.get('APPID')
        self.ucs = Tables.get('UCS')

    def _get_body(self):
        return DXFList( (DXFName('TABLES'),
                          self.linetypes,
                          self.layers,
                          self.styles,
                          self.views,
                          self.appids,
                          self.viewports,
                          self.ucs,
                          ) )

class Blocks(_Section):
    def __init__(self):
        self.blocks = {}

    def _get_body(self):
        body = DXFList()
        body.append(DXFName('BLOCKS'))
        body.extend(self.blocks.values())
        return body

    def add(self, block):
        blockname = block['name']
        self.blocks[blockname] = block

    def find(self, blockname):
        return self.blocks[blockname]

    def find_attdef(self, tag, blockname):
        block = self.find(blockname)
        return block.find_attdef(tag)

class Entities(_Section):
    def __init__(self):
        self.entities = DXFList()

    def _get_body(self):
        return DXFList( (DXFName('ENTITIES'),
                          self.entities))

    def add(self, entity):
        self.entities.append(entity)
