#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: insert block references with appended attributes
# Created: 11.04.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3
"""
Provides the Insert2 composite-entity.

Insert a new block-reference with auto-creating of attribs from attdefs,
and setting attrib-text by the attribs-dict.
"""

from dxfwrite.entities import Insert
import dxfwrite.const as const

__all__ = ['Insert2']

class Insert2(object):
    """
    Insert a new block-reference with auto-creating of attribs from attdefs,
    and setting attrib-text by the attribs-dict.
    """
    def __init__(self, blockdef, insert, attribs, rotation=0,
                 xscale=1., yscale=1., zscale=1.,
                 layer=const.BYBLOCK, color=const.BYLAYER, linetype=None):
        """
        kwargs
        ------

        blockdef -- the block definition itself
        insert -- insert point (xy- or xyz-tuple), z-axis is 0 by default
        xscale -- x-scale factor (float), default=1.
        yscale -- y-scale factor (float), default=1.
        zscale -- z-scale factor (float), default=1.
        rotation -- rotation angle in degree (float), default=0.
        attribs -- dict with tag:value pairs, to fill the the attdefs in the
            block-definition. example: {'TAG1': 'TextOfTAG1'}, create and insert
            an attrib from an attdef (with tag-value == 'TAG1'), and set
            text-value of the attrib to value 'TextOfTAG1'.

        Common kwargs
        -------------
        linetype, color, layer
        """
        self.blockdef = blockdef
        self.insert = insert
        self.attribs = attribs
        self.xscale = xscale
        self.yscale = yscale
        self.zscale = zscale
        self.rotation = rotation
        self.layer = layer
        self.color = color
        self.linetype = linetype

    def _build(self):
        def set_tags(insert_entity):
            for tag, text in self.attribs.items():
                try:
                    attdef = self.blockdef.find_attdef(tag)
                    attrib = attdef.new_attrib(text=text)
                    insert_entity.add(attrib, relative=True)
                except KeyError: # no attdef <tag> found
                    pass

        insert = Insert(blockname=self.blockdef['name'], insert=self.insert,
                        rotation=self.rotation,
                        layer=self.layer, color=self.color,
                        linetype=self.linetype)
        for key, value in [('xscale', self.xscale),
                           ('yscale', self.yscale),
                           ('zscale', self.zscale)]:
            if value != 1.:
                insert[key] = value

        set_tags(insert)
        return insert.__dxf__()

    def __dxf__(self):
        return self._build()