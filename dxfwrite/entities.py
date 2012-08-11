#!/usr/bin/env python
#coding:utf-8
# Purpose: entities R12
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import math

from dxfwrite.base import *
from dxfwrite.util import iterflatlist, set_flag
from dxfwrite.mixins import SubscriptAttributes

import dxfwrite.const as const

_DXF12_ENTITY_ATTRIBUTE_DEFINITION = {
    'LINE': {
        'start': AttribDef(DXFPoint3D, 0, priority=100),
        'end': AttribDef(DXFPoint3D, 1, 101),
        },
    'POINT': {
        'point': AttribDef(DXFPoint3D, 0, priority=100),
        'orientation': AttribDef(DXFAngle, 50, 101),
        },
    'CIRCLE': {
        'center': AttribDef(DXFPoint3D, 0, priority=100),
        'radius': AttribDef(DXFFloat, 40, 101),
        },
    'ARC': {
        'center': AttribDef(DXFPoint3D, 0, priority=100),
        'radius': AttribDef(DXFFloat, 40, 101),
        'startangle': AttribDef(DXFFloat, 50, 102),
        'endangle': AttribDef(DXFFloat, 51, 103),
        },
    'SHAPE': {
        'insert': AttribDef(DXFPoint3D, 0, 100),
        'name': AttribDef(DXFString, 2, 110),
        'rotation': AttribDef(DXFAngle, 50, 115),
        'xscale': AttribDef(DXFFloat, 41, 120),
        'oblique': AttribDef(DXFAngle, 51, 125),
        },
    'SOLID': { # drawing order 0->1->2->3->0
        0: AttribDef(DXFPoint3D, 0, priority=100),
        1: AttribDef(DXFPoint3D, 1, 101),
        2: AttribDef(DXFPoint3D, 3, 102), # (13, 23, 33) is drawn before (12, 22, 32) !!!
        3: AttribDef(DXFPoint3D, 2, 103),
        },
    'TRACE': { # drawing order 0->1->2->3->0
        0: AttribDef(DXFPoint3D, 0, priority=100),
        1: AttribDef(DXFPoint3D, 1, 101),
        2: AttribDef(DXFPoint3D, 3, 102),# (13, 23, 33) is drawn before (12, 22, 32) !!!
        3: AttribDef(DXFPoint3D, 2, 103),
        },
    'TEXT': {
        'insert': AttribDef(DXFPoint3D, 0, priority=100),
        'height': AttribDef(DXFFloat, 40, 105),
        'text': AttribDef(DXFString, 1, 110),
        'rotation': AttribDef(DXFAngle, 50, 115),
        'xscale': AttribDef(DXFFloat, 41, 120),
        'oblique': AttribDef(DXFAngle, 51, 125),
        'style': AttribDef(DXFString, 7, 130),
        'mirror': AttribDef(DXFInt, 71, 135),
        'halign': AttribDef(DXFInt, 72, 140),
        'valign': AttribDef(DXFInt, 73, 145),
        'alignpoint': AttribDef(DXFPoint3D, 1, 150),
        },
    'BLOCK': {
        'name': AttribDef(DXFString, 2, priority=100),
        'name2': AttribDef(DXFString, 3, 105),
        'flags': AttribDef(DXFInt, 70, 110),
        'basepoint': AttribDef(DXFPoint3D, 0, 115),
        'xref': AttribDef(DXFString, 1, 120),
        },
    'INSERT': {
        'attribs_follow': AttribDef(DXFInt, 66, priority=100),
        'blockname': AttribDef(DXFName, 2, 105),
        'insert': AttribDef(DXFPoint3D, 0, 110),
        'xscale': AttribDef(DXFFloat, 41, 115),
        'yscale': AttribDef(DXFFloat, 42, 120),
        'zscale': AttribDef(DXFFloat, 43, 125),
        'rotation': AttribDef(DXFAngle, 50, 130),
        'columns': AttribDef(DXFInt, 70, 135),
        'rows': AttribDef(DXFInt, 71, 140),
        'colspacing': AttribDef(DXFFloat, 44, 145),
        'rowspacing': AttribDef(DXFFloat, 45, 150),
        },
    'ATTRIB' : {
        'insert': AttribDef(DXFPoint3D, 0, priority=100),
        'height': AttribDef(DXFFloat, 40, 105),
        'text': AttribDef(DXFString, 1, 107),
        'tag': AttribDef(DXFString, 2, 112),
        'flags': AttribDef(DXFInt, 70, 115),
        'length': AttribDef(DXFInt, 73, 120),
        'rotation': AttribDef(DXFAngle, 50, 125),
        'xscale': AttribDef(DXFFloat, 41, 130),
        'oblique': AttribDef(DXFFloat, 51, 135),
        'style': AttribDef(DXFString, 7, 140),
        'mirror': AttribDef(DXFInt, 71, 145),
        'halign': AttribDef(DXFInt, 72, 150),
        'valign': AttribDef(DXFInt, 74, 155),
        'alignpoint': AttribDef(DXFPoint3D, 1, 160),
        },
    'ATTDEF' : {
        'insert': AttribDef(DXFPoint3D, 0, priority=100),
        'height': AttribDef(DXFFloat, 40, 105),
        'text': AttribDef(DXFString, 1, 107),
        'prompt': AttribDef(DXFString, 3, 111),
        'tag': AttribDef(DXFString, 2, 113),
        'flags': AttribDef(DXFInt, 70, 115),
        'length': AttribDef(DXFInt, 73, 120),
        'rotation': AttribDef(DXFAngle, 50, 125),
        'xscale': AttribDef(DXFFloat, 41, 130),
        'oblique': AttribDef(DXFFloat, 51, 135),
        'style': AttribDef(DXFString, 7, 140),
        'mirror': AttribDef(DXFInt, 71, 145),
        'halign': AttribDef(DXFInt, 72, 150),
        'valign': AttribDef(DXFInt, 74, 155),
        'alignpoint':AttribDef(DXFPoint3D, 1, 160),
        },
    '3DFACE': { # drawing order 0->1->2->3->0
        0: AttribDef(DXFPoint3D, 0, priority=100),
        1: AttribDef(DXFPoint3D, 1, 101),
        2: AttribDef(DXFPoint3D, 2, 102),
        3: AttribDef(DXFPoint3D, 3, 103),
        'flags': AttribDef(DXFInt, 70, 110),
        },
    'POLYLINE':{
        'vertices_follow': AttribDef(DXFInt, 66, priority=100), # always 1
        'polyline_elevation': AttribDef(DXFPoint3D, 0, priority=105), # there is also a common attrib elevation!!
        'flags': AttribDef(DXFInt, 70, priority=110),
        'startwidth': AttribDef(DXFFloat, 40, priority=115),
        'endwidth': AttribDef(DXFFloat, 41, priority=120),
        'mcount': AttribDef(DXFInt, 71, priority=125),
        'ncount': AttribDef(DXFInt, 72, priority=130),
        'msmooth_density': AttribDef(DXFInt, 73, priority=135),
        'nsmooth_density': AttribDef(DXFInt, 74, priority=140),
        'smooth_surface': AttribDef(DXFInt, 75, priority=145),
        },
    'VERTEX':{
        'location': AttribDef(DXFPoint3D, 0, priority=100),
        'startwidth': AttribDef(DXFFloat, 40, priority=105),
        'endwidth': AttribDef(DXFFloat, 41, priority=110),
        'bulge': AttribDef(DXFFloat, 42, priority=115),
        'flags': AttribDef(DXFFloat, 70, priority=120),
        'curve_fit_tangent_direction': AttribDef(DXFAngle, 50, priority=125),
        # vertex used to describe a face, face is drawn in order 0->1->2->3:
        0: AttribDef(DXFFloat, 71, priority=130), # face[0] .. first vertex
        1: AttribDef(DXFFloat, 72, priority=131), # face[1] .. second vertex
        2: AttribDef(DXFFloat, 73, priority=132), # face[2] .. third vertex
        3: AttribDef(DXFFloat, 74, priority=133), # face[3] .. fourth vertex
        },
    'VIEWPORT':{
        'center_point': AttribDef(DXFPoint3D, 0, 101),
        'width': AttribDef(DXFFloat, 40, priority=105),
        'height': AttribDef(DXFFloat, 41, priority=106),
        'status': AttribDef(DXFFloat, 68, priority=107),
        'id': AttribDef(DXFFloat, 69, priority=108),
        }, # and much more extended data, see class ViewportExtendedDXFTags()

    }

def _add_common_attribs(attribute_definition):
    common_attribs = {
        'linetype': AttribDef(DXFString, 6, priority=20),
        'elevation': AttribDef(DXFFloat, 38, priority=30),
        'thickness': AttribDef(DXFFloat, 39, priority=35),
        'color': AttribDef(DXFInt, 62, priority=40),
        'layer': AttribDef(DXFString, 8, priority=45),
        'paper_space': AttribDef(DXFInt, 67, priority=50),
        'extrusion_direction': AttribDef(DXFPoint, 200, priority=55),
    }
    for entry in attribute_definition.values():
        entry.update(common_attribs)

_add_common_attribs(_DXF12_ENTITY_ATTRIBUTE_DEFINITION)

class _Entity(object):
    DXF_ENTITY_NAME = 'ABSTRACT'
    DXF_ATTRIBUTES = {}

    def __init__(self, **kwargs):
        self.attribs = {}
        self['layer'] = '0' # set default layer
        # set attribs from kwargs
        for key, value in kwargs.items():
            # linetype can be None which means BYLAYER!
            # and BYLAYER is defined as linetype is omitted
            if value is not None:
                self[key] = value

    def is_valid_attribute_name(self, key):
        """ True if an AttribDef for key exists. """
        return key in self.DXF_ATTRIBUTES

    def __setitem__(self, key, value):
        if self.is_valid_attribute_name(key):
            self.attribs[key] = self._get_dxf_atom(key, value) # factory is called
        else:
            raise KeyError("Invalid attribute '%s' for Entity '%s'." % (str(key), self.__class__.__name__))

    def __getitem__(self, key):
        if self.is_valid_attribute_name(key):
            element = self.attribs[key]
            try:
                return element.value # DXFAtom
            except AttributeError:
                return element # DXFList or list or tuple or DXFPoint
        else:
            raise KeyError("Invalid attribute '%s' for Entity '%s'." % (str(key), self.__class__.__name__))

    def _get_dxf_atom(self, attribname, value):
        """ create an object for attribname by factory from attribute_definition """
        attrib = self.DXF_ATTRIBUTES[attribname]
        return attrib.factory(value, attrib.group_code)

    def _priority(self, key):
        """ get priority of attribute key """
        return self.DXF_ATTRIBUTES[key].priority

    def get_attribs(self):
        """ get attribs sorted by priority """
        priority_attribs = [ (self._priority(key), value)
                 for key, value in self.attribs.items() ]
        return [ value for priority, value  in sorted(priority_attribs) ]

    def get_data(self): # abstract
        # example: block->content, polyline->vertices, faces, insert->attribs
        return DXFList()

    def valid(self):
        """ Validate object before dxf output. """
        return True

    def extension_point(self): # abstract
        """ general extension point, first call in __dxftags__.
        """
        pass

    def __dxf__(self):
        """ Create the dxf string. """
        return dxfstr(self.__dxftags__())

    def __dxftags__(self):
        self.extension_point() # last chance to manipulate the entity
        if self.valid():
            dxftags = DXFList()
            dxftags.append(DXFAtom(self.DXF_ENTITY_NAME))
            dxftags.extend(self.get_attribs()) # attribs sorted by priority
            dxftags.extend(self.get_data()) # example: block->content, polyline->vertices, faces, insert->attribs
            return dxftags
        else:
            raise DXFValidationError("invalid or missing attributes in object '%s'." % self.__class__.__name__)


class Line(_Entity):
    DXF_ENTITY_NAME = 'LINE'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['LINE']

    def __init__(self, **kwargs):
        default = {
            'start': (0,0),
            'end': (0,0),
        }
        default.update(kwargs)
        super(Line, self).__init__(**default)


class Point(_Entity):
    DXF_ENTITY_NAME = 'POINT'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['POINT']

    def __init__(self, **kwargs):
        default = {
            'point': (0,0),
        }
        default.update(kwargs)
        super(Point, self).__init__(**default)

class Solid(_Entity):
    DXF_ENTITY_NAME = 'SOLID'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['SOLID']

    def __init__(self, points=[], **kwargs):
        super(Solid, self).__init__(**kwargs)
        self.set_points(points)

    def set_points(self, points):
        for key, point in enumerate( points):
            self[key] = point

    def extension_point(self):
        if 3 not in self.attribs:
            try: # set point self[3] equal to point self[2]
                self[3] = self[2]['xyz'] # has to be a tuple
            except KeyError: # valid() fails if self[2] does not exist
                pass

    def valid(self):
        for key in (0, 1, 2, 3):
            if key not in self.attribs:
                return False
        return True

class Trace(Solid):
    DXF_ENTITY_NAME = 'TRACE'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['TRACE']

class Face3D(Solid):
    DXF_ENTITY_NAME = '3DFACE'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['3DFACE']

class Shape(_Entity):
    DXF_ENTITY_NAME = 'SHAPE'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['SHAPE']

    def __init__(self, **kwargs):
        default = {
            'insert': (0, 0),
            }
        default.update(kwargs)
        super(Shape, self).__init__(**default)

class Text(_Entity):
    DXF_ENTITY_NAME = 'TEXT'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['TEXT']

    def __init__(self, **kwargs):
        default = {
            'insert': (0, 0),
            'height': 1,
            'text': 'Text',
            }
        default.update(kwargs)
        super(Text, self).__init__(**default)

class Arc(_Entity):
    DXF_ENTITY_NAME = 'ARC'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['ARC']

    def __init__(self, **kwargs):
        default = {
            'center': (0,0),
            'radius': 1,
            'startangle': 0,
            'endangle': 360,
        }
        default.update(kwargs)
        super(Arc, self).__init__(**default)

class Circle(_Entity):
    DXF_ENTITY_NAME = 'CIRCLE'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['CIRCLE']

    def __init__(self, **kwargs):
        default = {
            'center': (0, 0),
            'radius': 1,
        }
        default.update(kwargs)
        super(Circle, self).__init__(**default)

class Insert(_Entity):
    """ The INSERT entity insert a block reference to a drawing or block, you
    can add attributes with the :meth:add() method.

    """
    DXF_ENTITY_NAME = 'INSERT'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['INSERT']

    def __init__(self, **kwargs):
        default = {
            'insert': (0, 0), # the default location
        }
        default.update(kwargs)
        super(Insert, self).__init__(**default)
        self.data = DXFList()

    def add(self, attrib, relative=True, block_basepoint=None):
        """ Add attributes to the block reference. The position in attrib is
        an absolute location in WCS, or relative to the block origin (rotation
        is relative to the block x-axis). All angles in degrees.

        :param attrib: the :class:Attrib instance
        :param bool relative: Insert the attrib relative to the block origin.
        :param block_basepoint: the basepoint of the block, its the basepoint
            for scaling and rotating of the attribute.
        """
        def move_attrib_insert_point_to_basepoint(reverse=False):
            if block_basepoint is None:
                return attrib_insert
            direction = -1 if reverse else +1
            return tuple( (attrib_insert[axis] - block_basepoint[axis] * direction
                           for axis in range(len(attrib_insert))) )

        def get_scale_values():
            scale1 = DXFFloat(1.)
            return [self.attribs.get(value_name, scale1).value for value_name in ('xscale', 'yscale', 'zscale')]

        def scale():
            scale_values = get_scale_values()
            font_scaling(scale_values[0], scale_values[1])
            return tuple( (attrib_insert[axis] * scale_values[axis]
                           for axis in range(len(attrib_insert))) )

        def font_scaling(xscale, yscale):
            if yscale != 1.:
                attrib['height'] = attrib['height'] * yscale

            distort = round(xscale/yscale, 5)
            if distort != 1.0:
                attrib['xscale'] = attrib['xscale'] * distort

        def rotate():
            new_angle = math.radians(insert_angle) + math.atan2(attrib_insert[1], attrib_insert[0])
            radius = math.hypot(attrib_insert[0], attrib_insert[1])
            return (radius * math.cos(new_angle), radius * math.sin(new_angle), 0. )

        def get_world_coordinates():
            basepoint = (0., 0., 0.) if block_basepoint is None else block_basepoint
            return tuple( (insert_insert[axis] + attrib_insert[axis] - basepoint[axis]
                           for axis in range(len(insert_insert))) )

        if relative is True:
            angel0 = DXFAngle(0.)
            attrib_insert = attrib['insert']['xyz']
            attrib_angle = attrib.attribs.get('rotation', angel0).value
            insert_insert = self['insert']['xyz']
            insert_angle = self.attribs.get('rotation', angel0).value

            attrib_insert = move_attrib_insert_point_to_basepoint()
            attrib_insert = scale()
            attrib_insert = rotate()
            attrib_insert = move_attrib_insert_point_to_basepoint(reverse=True)
            attrib_insert = get_world_coordinates()

            attrib['insert'] = attrib_insert
            attrib['alignpoint'] = attrib_insert
            attrib['rotation'] = insert_angle + attrib_angle
        self.data.append(attrib)

    def extension_point(self):
        if len(self.data):
            self['attribs_follow'] = 1

    def get_data(self):
        if len(self.data):
            if not self.data.endswith('SEQEND'):
                self.data.append(DXFAtom('SEQEND'))
        return self.data

class Attdef(_Entity):
    """ The ATTDEF entity defines the characteristic of an ATTRIB entity
    (template). The Attdef object resides in the BLOCK definition entity::

        blockdef.add(attdef)

    """
    DXF_ENTITY_NAME = 'ATTDEF'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['ATTDEF']

    def __init__(self, **kwargs):
        default = {
            'insert': (0,0),
            'height': 1,
            'text': 'Attrib',
            'prompt': 'Input:',
            'tag': 'ATTRIB',
            'flags': 0,
        }
        default.update(kwargs)
        super(Attdef, self).__init__(**default)

    def new_attrib(self, **kwargs):
        """ Create a new ATTRIB entity with this ATTDEF entity as template.

        :param kwargs: override the ATTDEF default values.
        """
        for key in self.attribs.keys():
            if key not in ('prompt', 'tag', 'insert', 'alignpoint'): # insert here attribs to ignore
                kwargs.setdefault(key, self[key]) # set key only if not present
        kwargs['tag'] = self['tag'] # has to be the same tag
        # special case for dxfpoints
        for pointname in ('insert', 'alignpoint'):
            if (pointname not in kwargs) and \
               (pointname in self.attribs):
                kwargs[pointname] = self[pointname]['xyz'] # get the tuple(x,y,z)
        return Attrib(**kwargs)

class Attrib(_Entity):
    """ The ATTRIB entity creates a text entity, which is mostly is appended
    to the INSERT entity. This are special text entities, because they can be
    evaluated by CAD programs and they can be exported for further processing
    by external programs (like Excel). They often (but must not) created by a
    ATTDEF template entity, which resides in the BLOCK definition entity.
    """
    DXF_ENTITY_NAME = 'ATTRIB'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['ATTRIB']

    def __init__(self, **kwargs):
        default = {
            'insert': (0,0),
            'height': 1,
            'text': 'Attrib',
            'tag': 'ATTRIB',
            'flags': 0,
            }
        default.update(kwargs)
        super(Attrib, self).__init__(**default)

class Block(_Entity):
    """ BLOCK definition entity. This block definition can be referenced
    (inserted) by the INSERT entity. It can contain ATTDEF entities, which are
    templates for the ATTRIB entities used by the INSERT entity.
    """
    DXF_ENTITY_NAME = 'BLOCK'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['BLOCK']

    def __init__(self, **kwargs):
        """ Block constructor.
        """
        default = {
            'name': 'empty',
            'flags': 0,
            'basepoint': (0,0),
        }
        default.update(kwargs)
        super(Block, self).__init__(**default)
        self.data = DXFList()

    def find_attdef(self, tag):
        """ Find ATTDEF entities in the block definition, which can occur on
        arbitrary places.
        """
        for entity in iterflatlist(self.data): # flat data list
            if isinstance(entity, _Entity) and \
                (entity.DXF_ENTITY_NAME == 'ATTDEF') and \
                (entity['tag'] == tag):
                return entity
        raise KeyError("no attdef with tag '%s' found!" % str(tag))

    def add(self, entity):
        """ Add DXF entities to the block definition, like you would do it at
        drawings.
        """
        self.data.append(entity)

    def extension_point(self):
        self['name2'] = self['name']
        if not self.valid():
            self.data.extend(self.blockend())

    def blockend(self):
        return [DXFAtom('ENDBLK')]

    def valid(self):
        if not len(self.data):
            return False
        else:
            return self.data.endswith('ENDBLK')

    def get_data(self):
        return self.data

class Polyline(_Entity):
    """ POLYLINE entity to create 2D and 3D polylines (some vertices connected
    by lines), but also to create Polymeshes and Polyfaces, see special
    classes below.

    Public attributes:

    .. attribute:: vertices

    """
    DXF_ENTITY_NAME = 'POLYLINE'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['POLYLINE']

    def __init__(self, points=[], **kwargs):
        """ Polyline constructor.

        :param points: list of points, 2D or 3D points, z-value of 2D points is 0.
        """
        default = {
            'vertices_follow': 1,
            'polyline_elevation': (0, 0, 0),
            'flags': const.POLYLINE_3D_POLYLINE,
        }
        default.update(kwargs)
        super(Polyline, self).__init__(**default)
        self.vertices = DXFList()
        self.add_vertices(points)

    def close(self, status=True):
        """ Close Polyline: first vertex is connected with last vertex.

        :param bool status: True for closed polyline; False for open polyline.
        """
        self['flags'] = set_flag(self['flags'], const.POLYLINE_CLOSED, status)

    def add_vertex(self, point, **kwargs):
        """ Add a vertex located at point to the polyline.

        :param point: is a (x, y) or (x, y, z) tuple, z-value of a 2D point is 0.
        """
        self.vertices.append(Vertex(location=point, **kwargs))

    def add_vertices(self, points):
        """ Add a list of vertices.

        :param points: list of points, 2D or 3D points, z-value of 2D points is 0.
        """
        for point in points:
            self.add_vertex(point)

    def extension_point(self):
        if not self.valid():
            self.vertices.append(DXFAtom('SEQEND'))

    def valid(self):
        if len(self.vertices) == 0:
            return False
        else:
            return self.vertices.endswith('SEQEND')

    def get_data(self):
        return self.vertices


class Polymesh(_Entity):
    """ Special case of POLYLINE, creates a m(rows) x n(cols) Polymesh, each
    column has m vertices and each row has n vertices. All mesh indices are
    zero based.
    """
    DXF_ENTITY_NAME = 'POLYLINE' # a polymesh is also a polyline
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['POLYLINE']

    def __init__(self, nrows, ncols, **kwargs):
        """ Polymesh constructor.

        constraints: 2 <= nrows <= 256; 2 <= ncols <= 256
        I do not check this, because it is a product specific limitation by
        AutoCAD.
        """
        default = {
            'vertices_follow': 1,
            'mcount': nrows,
            'ncount': ncols,
            'flags': const.POLYLINE_3D_POLYMESH,
        }
        default.update(kwargs)
        super(Polymesh, self).__init__(**default)
        self.vertices = {}

    def set_mclosed(self, status):
        flags = self['flags']
        self['flags'] = set_flag(flags, const.POLYLINE_MESH_CLOSED_M_DIRECTION,
                                 status)
    def set_nclosed(self, status):
        flags = self['flags']
        self['flags'] = set_flag(flags, const.POLYLINE_MESH_CLOSED_N_DIRECTION,
                                 status)

    def _build_vertex(self, point):
        return Vertex(location=point, flags=const.VTX_3D_POLYGON_MESH_VERTEX)

    def set_vertex(self, row, col, point):
        """ Set location of vertex (row, col).

        :param int row: zero based mesh index
        :param in col: zero based mesh index
        :param point: vertex location as (x, y, z) tuple
        """
        self.vertices[(row, col)] = self._build_vertex(point)

    def get_vertices(self):
        vertex0 = Vertex(location=(0,0,0)) # default point
        return ( self.vertices.get( (row,col), vertex0)
                 for row in xrange(self['mcount'])
                 for col in xrange(self['ncount'])
                 )

    def get_data(self):
        data = DXFList(self.get_vertices())
        data.append(DXFAtom('SEQEND'))
        return data


class Polyface(_Entity):
    """ Another special case of POLYLINE, to create a freeform 3D object,
    which consist of arbitrary count of faces.
    """
    DXF_ENTITY_NAME = 'POLYLINE' # a polyface is also a polyline
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['POLYLINE']

    def __init__(self, precision=6, **kwargs):
        """ Polyface constructor.
        """
        default = {
            'vertices_follow': 1,
            'flags': const.POLYLINE_POLYFACE,
        }
        default.update(kwargs)
        super(Polyface, self).__init__(**default)
        self.precision = precision
        self.vertices = DXFList()
        self.faces = DXFList()
        self.point2index = {}

    def _build_vertex(self, point):
        return Vertex(location=point,
                      flags=const.VTX_3D_POLYGON_MESH_VERTEX + \
                      const.VTX_3D_POLYFACE_MESH_VERTEX)

    def _build_face(self, color):
        return Vertex(flags=const.VTX_3D_POLYFACE_MESH_VERTEX, color=color)
    # do not delete 'location' for the face-vertex, it is needed,
    # even though it is always (0,0,0), tested with AutoCAD

    def add_face(self, vertices, color=0):
        """ This is the recommend method for adding faces.

        :param vertices: is a list or tuples with 3 or 4 points (x, y, z).
        :param int color: range [1..255], 0 = **BYBLOCK**, 256 = **BYLAYER**
        """
        # len-check prevents usage of generators!
        # if len(vertices) not in (3, 4): raise ValueError
        self.add_face_by_indices(
            (self.add_vertex(point) for point in vertices),
            color)

    def add_vertex(self, point):
        """ Add a point to vertices and return the index of the vertex.

        :param point: vertex location as (x, y, z) tuple
        """
        def key(point):
            """ Vertex key with reduced floating point precision, near points
            will reference the same vertex. This reduces the vertices count, but
            it also reduces the accuracy of the model, use this wisely. You can
            control the function by the parameter self.precision, which determines
            the floating point precision.

            remember: only the key has reduced precision not the point itself. !!!
            """
            return tuple( [round(coord, self.precision) for coord in point] )

        try:
            index = self.point2index[key(point)] # use existing vertex
        except KeyError: # add new point
            index = len(self.vertices)
            self.vertices.append(self._build_vertex(point))
            self.point2index[key(point)] = index
        return index

    def add_face_by_indices(self, indices, color=0):
        """ indices is a list or tuple of vertex indices (got from add_vertex).
        """
        face = self._build_face(color)
        for (key, vertex_index) in enumerate(indices):
            face[key] = vertex_index + 1 # dxf index is 1 based
        self.faces.append(face)

    def extension_point(self):
        self['mcount'] = len(self.vertices)
        self['ncount'] = len(self.faces)

    def get_data(self):
        return DXFList( [self.vertices, self.faces, DXFAtom('SEQEND')] )


class Vertex(_Entity):
    """ The VERTEX entity is only for internal usage by Polyline, Polymesh and
    Polyface.
    """
    DXF_ENTITY_NAME = 'VERTEX'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['VERTEX']

    def __init__(self, **kwargs):
        default = {
            'location': (0, 0, 0),
        }
        default.update(kwargs)
        super(Vertex, self).__init__(**default)


class Viewport(_Entity):
    """ The VIEWPORT entity creates viewports in paper space, this viewports
    shows a part of the model space. It is a tool to design the drawing layout.
    """
    DXF_ENTITY_NAME = 'VIEWPORT'
    DXF_ATTRIBUTES = _DXF12_ENTITY_ATTRIBUTE_DEFINITION['VIEWPORT']
    viewport_id = 2 # notes to id:
    # The id of the first viewport has to be 1, which is the definition of
    # paper space, see also Drawing.default_settings. For the following
    # viewports it seems only important, that the id is greater than 1.

    def __init__(self, center_point, width, height, **kwargs):
        self.extended_dxf_tags = ViewportExtendedDXFTags()
        default = {
            'status': 1, # by default highest priority (stack order)
            'id': Viewport.viewport_id, # with auto increment, user should not care about it
            'layer': "VIEWPORTS", # use separated layer to turn off for plotting
            'paper_space': 1, # should always be placed in the paper space
            'center_point': center_point,
            'width': width,
            'height': height,
            }
        default.update(kwargs)
        super(Viewport, self).__init__(**default)
        Viewport.viewport_id += 1

    def get_data(self):
        # build extended entity group
        return self.extended_dxf_tags.get_dxf_tags()

    def __getitem__(self, item):
        if item in self.extended_dxf_tags:
            return self.extended_dxf_tags[item]
        else:
            return super(Viewport, self).__getitem__(item)

    def __setitem__(self, key, value):
        if key in self.extended_dxf_tags:
            self.extended_dxf_tags[key] = value
        else:
            super(Viewport, self).__setitem__(key, value)


class ViewportExtendedDXFTags(SubscriptAttributes):
    """ Helper class for Viewport().

    This class defines the extended dxf tags, which can not be treated as AttibDef()
    like the 'ordinary' dxf tags, because:

        - the group codes of this tags are not unique (see: get_dxf_tags())
        - this tags must occur in a particular order, the order of their appearing,
          defines their meaning.

    """
    def __init__(self):
        # view_target_point & view_direction_vector defines the view direction
        # only important for 3D model views
        self.view_target_point =  (0., 0., 0.)
        self.view_direction_vector = (0., 0., 0.)
        self.view_twist_angle = 0. # in radians!!!
        self.view_height = 1. # height of model space area
        self.view_center_point = (0., 0.) # point in model space, which is displayed in the viewport center.
        self.perspective_lens_length = 50.
        self.front_clip_plane_z_value = 0.
        self.back_clip_plane_z_value = 0.
        self.view_mode = 0
        self.circle_zoom = 100
        self.fast_zoom = 1
        self.ucs_icon = 3
        self.snap = 0
        self.grid = 0
        self.snap_style = 0
        self.snap_isopair = 0
        self.snap_angle = 0.
        self.snap_base_point = (0., 0.)
        self.snap_spacing = (0.1, 0.1)
        self.grid_spacing = (0.1, 0.1)
        self.hidden_plot = 0

    def get_dxf_tags(self):
        return DXFList(
            [
                DXFString('ACAD', 1001),
                DXFString('MVIEW', 1000),
                DXFString('{', 1002),
                DXFInt(16, 1070), # extended data version, always 16 for R11/12
                DXFPoint(self.view_target_point, 1000),
                DXFPoint(self.view_direction_vector, 1000),
                DXFFloat(self.view_twist_angle, 1040),
                DXFFloat(self.view_height, 1040),
                DXFFloat(self.view_center_point[0], 1040),
                DXFFloat(self.view_center_point[1], 1040),
                DXFFloat(self.perspective_lens_length, 1040),
                DXFFloat(self.front_clip_plane_z_value, 1040),
                DXFFloat(self.back_clip_plane_z_value, 1040),
                DXFInt(self.view_mode, 1070),
                DXFInt(self.circle_zoom, 1070),
                DXFInt(self.fast_zoom, 1070),
                DXFInt(self.ucs_icon, 1070),
                DXFInt(self.snap, 1070),
                DXFInt(self.grid, 1070),
                DXFInt(self.snap_style, 1070),
                DXFInt(self.snap_isopair, 1070),
                DXFFloat(self.snap_angle, 1040),
                DXFFloat(self.snap_base_point[0], 1040),
                DXFFloat(self.snap_base_point[1], 1040),
                DXFFloat(self.snap_spacing[0], 1040),
                DXFFloat(self.snap_spacing[1], 1040),
                DXFFloat(self.grid_spacing[0], 1040),
                DXFFloat(self.grid_spacing[1], 1040),
                DXFInt(self.hidden_plot, 1070),
                DXFString('{', 1002), # frozen layer list is empty
                DXFString('}', 1002),
                DXFString('}', 1002), # end viewport data
            ]
        )

