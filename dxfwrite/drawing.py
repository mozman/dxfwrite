#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: Drawing R12
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3


from cStringIO import StringIO

from dxfwrite import DXFEngine
from dxfwrite.base import *
from dxfwrite.sections import Sections

import dxfwrite.const as const


import std

class Drawing(object):
    """ Collection of dxf entities. """
    def __init__(self, name='noname.dxf', default_values=True):
        self.filename = name
        self.header = Sections.get('HEADER')
        self.tables = Sections.get('TABLES')
        self.blocks = Sections.get('BLOCKS')
        self.entities = Sections.get('ENTITIES')
        self._anonymous_counter = 0

        if default_values:
            self.add_default_values()

    @property
    def linetypes(self): return self.tables.linetypes
    @property
    def layers(self): return self.tables.layers
    @property
    def styles(self): return self.tables.styles
    @property
    def views(self): return self.tables.views
    @property
    def viewports(self): return self.tables.viewports
    @property
    def ucs(self): return self.tables.ucs

    def __dxf__(self):
        with StringIO() as fp:
            self._write_dxf(fp)
            return fp.getvalue()

    def _write_dxf(self, fp):
        fp.write(dxfstr(self.header))
        fp.write(dxfstr(self.tables))
        fp.write(dxfstr(self.blocks))
        fp.write(dxfstr(self.entities))
        fp.write(dxfstr(DXFAtom('EOF')))

    def add(self, entity): # shortcut for Drawing.entities.add()
        """ add an entity """
        self.entities.add(entity)
        return entity

    def anonymous_blockname(self, typechar):
        """ create an anonymous block name

        typechar
            U = *U### anonymous blocks
            E = *E### anonymous non-uniformly scaled blocks
            X = *X### anonymous hatches
            D = *D### anonymous dimensions
            A = *A### anonymous groups
        """
        self._anonymous_counter += 1
        return "*{0}{1}".format(typechar, self._anonymous_counter)

    def add_anonymous_block(self, entity, layer="0", typechar='U'):
        """ insert entity (can be a DXFList) as anonymous block
        into  drawing
        """
        blockname = self.anonymous_blockname(typechar)
        block = DXFEngine.block(blockname, basepoint=(0, 0),
                                flags=const.BLK_ANONYMOUS)
        block.add(entity)
        self.blocks.add(block)
        insert = DXFEngine.insert(blockname, insert=(0, 0), layer=layer)
        self.add(insert)
        return blockname

    def add_default_values(self):
        self.header.add_vars([
            ('$ACADVER', DXFString('AC1009')),
            ('$INSBASE', DXFPoint()),
            ('$EXTMIN', DXFPoint()),
            ('$EXTMAX', DXFPoint(( 100, 100, 0) )),
            ])
        for ltype in self.std_linetypes():
            self.linetypes.add(ltype)
        for style in self.std_styles():
            self.styles.add(style)
        self.tables.appids.add(DXFEngine.appid('DXFWRITE') )

    def save(self):
        with open(self.filename, 'w') as fp:
            self._write_dxf(fp)

    def saveas(self, name):
        self.filename = name
        self.save()

    def add_layer(self, name, **kwargs):
        layer = DXFEngine.layer(name, **kwargs)
        self.layers.add(layer)
        return layer

    def add_style(self, name, **kwargs):
        style = DXFEngine.style(name, **kwargs)
        self.styles.add(style)
        return style

    def add_linetype(self, name, **kwargs):
        linetype=DXFEngine.linetype(name, **kwargs)
        self.linetypes.add(linetype)
        return linetype

    def add_view(self, name, **kwargs):
        view = DXFEngine.view(name, **kwargs)
        self.views.add(view)
        return view

    def add_viewport(self, name, **kwargs):
        viewport = DXFEngine.viewport(name, **kwargs)
        self.viewports.add(viewport)
        return viewport

    def add_ucs(self, name, **kwargs):
        ucs = DXFEngine.ucs(name, **kwargs)
        self.ucs.add(ucs)
        return ucs

    def std_linetypes(self):
        """ create standard linetypes """
        return [DXFEngine.linetype(
            name, description=desc,
            pattern=DXFEngine.linepattern(pat))
                for name, desc, pat in std.linetypes()]

    def std_styles(self):
        """ create standard text styles """
        return [DXFEngine.style(name, font=f) for name, f in std.styles() ]
