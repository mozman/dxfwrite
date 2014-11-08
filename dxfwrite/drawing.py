#!/usr/bin/env python
# coding:utf-8
# Purpose: Drawing R12
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import os

from . import DXFEngine
from .base import *
from .sections import create_section
from . import const
from . import std


class Drawing(object):
    """ The Drawing object manages all the necessary sections, like header, tables
    and blocks. The tables-attribute contains the layers, styles, linetypes and
    other tables.
    
    """
    ENCODING = 'cp1252'

    def __init__(self, name='noname.dxf'):
        """ Drawing constructor.

        :param str name: filename of drawing
        """
        self.filename = name
        self.header = create_section('HEADER')
        self.tables = create_section('TABLES')
        self.blocks = create_section('BLOCKS')
        self.entities = create_section('ENTITIES')
        self.modelspace = ModelSpaceProxy(self.entities)
        self.paperspace = PaperSpaceProxy(self.entities)
        self._anonymous_counter = 0
        self.default_settings()

    @property
    def linetypes(self):
        return self.tables.linetypes

    @property
    def layers(self):
        return self.tables.layers

    @property
    def styles(self):
        return self.tables.styles

    @property
    def views(self):
        return self.tables.views

    @property
    def viewports(self):
        return self.tables.viewports

    @property
    def ucs(self):
        return self.tables.ucs

    def __dxf__(self):
        """ Returns the drawing DXF content as string.
        """
        return tags2str(self)

    def __dxftags__(self):
        dxftags = DXFList()
        dxftags.append(self.header.__dxftags__())
        dxftags.append(self.tables.__dxftags__())
        dxftags.append(self.blocks.__dxftags__())
        dxftags.append(self.entities.__dxftags__())
        dxftags.append(DXFAtom('EOF'))
        return dxftags

    def add(self, entity):
        """ Add an entity to drawing.

        shortcut for: Drawing.entities.add()
        """
        self.entities.add(entity)
        return entity

    def anonymous_blockname(self, typechar):
        """ Create an anonymous block name.

        typechar
            U = *U### anonymous blocks
            E = *E### anonymous non-uniformly scaled blocks
            X = *X### anonymous hatches
            D = *D### anonymous dimensions
            A = *A### anonymous groups
        """
        self._anonymous_counter += 1
        return "*%s%s" % (str(typechar), str(self._anonymous_counter))

    def add_anonymous_block(self, entity, layer="0", typechar='U',
                            basepoint=(0, 0), insert=(0, 0)):
        """ Insert entity (can be a DXFList) as anonymous block into drawing.
        """
        blockname = self.anonymous_blockname(typechar)
        block = DXFEngine.block(blockname, basepoint=basepoint,
                                flags=const.BLK_ANONYMOUS)
        block.add(entity)
        self.blocks.add(block)
        insert = DXFEngine.insert(blockname, insert=insert, layer=layer)
        self.add(insert)
        return blockname

    def default_settings(self):
        self.header['$ACADVER'] = 'AC1009'
        self.header['$INSBASE'] = (0, 0, 0)
        self.header['$EXTMIN'] = (0, 0, 0)
        self.header['$EXTMAX'] = (100, 100, 0)
        self.header['$UNITMODE'] = 0  # for metric units in viewers
        self.header['$AUNITS'] = 0  # only for CAD programs relevant; DXF stores always in degrees (AutoCAD)
        # 0 = degrees (circle = 360 deg)
        # 1 = degree/minutes/seconds
        # 2 = gradians (circle = 400 grad)
        # 3 = radians (circle = 2*PI)
        # 4 = surveyor's units
        self.header['$ANGBASE'] = 0  # Angle 0 direction; 0=x-axis
        self.header['$ANGDIR'] = 0  # 0=counter-clockwise; 1 = clockwise

        for ltype in self.std_linetypes():
            self.linetypes.add(ltype)
        for style in self.std_styles():
            self.styles.add(style)
        self.tables.appids.add(DXFEngine.appid('DXFWRITE'))
        self.add_layer('DIMENSIONS')
        self.add_layer('TABLEBACKGROUND')
        self.add_layer('TABLECONTENT')
        self.add_layer('TABLEGRID')
        self.add_layer('VIEWPORTS', color=7)

        # Setup paper space, but I don't know the meaning of this VIEWPORT
        # entity, also the dimensions of this viewport seems not really
        # important, except status=1 and id=1.
        self.paperspace.add(DXFEngine.viewport((0, 0), 1, 1, status=1, id=1))

    def save(self):
        """ Write DXF data to file-system (Drawing.filename).
        """
        if PYTHON3:
            fileobj = open(self.filename, 'w', encoding=self.ENCODING, errors="replace")
        else:
            fileobj = open(self.filename, 'w')
        self.save_to_fileobj(fileobj)
        fileobj.close()

    def save_to_fileobj(self, fileobj):
        """ Write DXF data to a file-like object. (i.e. StringIO)
        """
        writetags(fileobj, self.__dxftags__(), self.ENCODING)

    def saveas(self, name):
        """ Set new filename and write DXF data to file-system.
        """
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
        linetype = DXFEngine.linetype(name, **kwargs)
        self.linetypes.add(linetype)
        return linetype

    def add_view(self, name, **kwargs):
        view = DXFEngine.view(name, **kwargs)
        self.views.add(view)
        return view

    def add_vport(self, name, **kwargs):
        vport = DXFEngine.vport(name, **kwargs)
        self.viewports.add(vport)
        return vport

    def add_ucs(self, name, **kwargs):
        ucs = DXFEngine.ucs(name, **kwargs)
        self.ucs.add(ucs)
        return ucs

    def std_linetypes(self):
        """ Create standard linetypes.
        """
        return [DXFEngine.linetype(
            name, description=desc,
            pattern=DXFEngine.linepattern(pat))
                for name, desc, pat in std.linetypes()]

    def std_styles(self):
        """ Create standard text styles.
        """
        return [DXFEngine.style(name, font=f) for name, f in std.styles()]

    def add_xref(self, filepath, insert=(0., 0., 0.), layer='0'):
        """ Create a simple XREF reference, `filepath` is the referenced
        drawing and `insert` is the insertion point.

        """

        def normblockname(blockname):
            for char in ' :/\\.':
                blockname = blockname.replace(char, '')
            return blockname

        dirname, filename = os.path.split(filepath)
        blockname = normblockname(filename)
        xref = DXFEngine.block(name=blockname, flags=const.BLK_XREF, xref=filepath)
        self.blocks.add(xref)
        self.add(DXFEngine.insert(blockname, insert, layer=layer))


class ModelSpaceProxy(object):
    LAYOUT = 0

    def __init__(self, entities):
        self._entities = entities

    def add(self, entity):
        entity['paper_space'] = self.LAYOUT
        self._entities.add(entity)
        return entity


class PaperSpaceProxy(ModelSpaceProxy):
    LAYOUT = 1

