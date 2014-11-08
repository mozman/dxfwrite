#coding:utf-8
# Purpose: sections R12
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

__all__ = ['create_section']

from .base import DXFAtom, DXFList, DXFName, dxfstr
from .tables import create_table
from . import hdrvars


def create_section(name):
    """ Sections factory.
    """
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
        return dxfstr(self.__dxftags__())

    def __dxftags__(self):
        return DXFList((
            DXFAtom('SECTION'),
            DXFList(self._get_body()),
            DXFAtom('ENDSEC')
        ))

    def _get_body(self):
        """ abstract """


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
        return DXFList((DXFName('HEADER'), DXFList(varlist)))

    def __getitem__(self, key):
        """ Get a header var by the subscript operator::

                value = drawing.header[varname]
        """
        return self.variables[key]

    def __setitem__(self, key, value):
        """ Set a header var by the subscript operator::

                drawing.header[varname] = value
        """
        self.variables[key] = hdrvars.Factory[key](value)


class TablesSection(_Section):
    def __init__(self):
        self.linetypes = create_table('LTYPE')
        self.layers = create_table('LAYER')
        self.styles = create_table('STYLE')
        self.views = create_table('VIEW')
        self.viewports = create_table('VPORT')
        self.appids = create_table('APPID')
        self.ucs = create_table('UCS')

    def _get_body(self):
        return DXFList((DXFName('TABLES'),
                        self.linetypes,
                        self.layers,
                        self.styles,
                        self.views,
                        self.appids,
                        self.viewports,
                        self.ucs,
        ))


class Blocks(_Section):
    def __init__(self):
        self.blocks = {}

    def _get_body(self):
        body = DXFList()
        body.append(DXFName('BLOCKS'))
        body.extend(self.blocks.values())
        return body

    def add(self, block):
        """ Add a BLOCK definition entity to the blocks section.
        """
        blockname = block['name']
        self.blocks[blockname] = block

    def find(self, blockname):
        """ Get BLOCK definition entity by name.
        """
        return self.blocks[blockname]

    def find_attdef(self, tag, blockname):
        """ Get ATTDEF entity by tag.
        """
        block = self.find(blockname)
        return block.find_attdef(tag)


class Entities(_Section):
    def __init__(self):
        self.entities = DXFList()

    def _get_body(self):
        return DXFList((DXFName('ENTITIES'), self.entities))

    def add(self, entity):
        """ Add a DXF entity to the entities section.
        """
        self.entities.append(entity)
