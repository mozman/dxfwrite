#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: entities R12
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3


import math

from dxfwrite.base import *
from dxfwrite.util import iterflatlist, set_flag
import dxfwrite.const as const

_DXF12_EntityAttributeDefinition = {
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
        }
    }

def _add_common_attribs():
    common_attribs = {
        'linetype': AttribDef(DXFString, 6, priority=20),
        'elevation': AttribDef(DXFFloat, 38, priority=30),
        'thickness': AttribDef(DXFFloat, 39, priority=35),
        'color': AttribDef(DXFInt, 62, priority=40),
        'layer': AttribDef(DXFString, 8, priority=45),
        'paper_space': AttribDef(DXFInt, 67, priority=50),
        'extrusion_direction': AttribDef(DXFPoint, 200, priority=55),
    }
    for key in _DXF12_EntityAttributeDefinition.keys(): # loop over entities
        _DXF12_EntityAttributeDefinition[key].update(common_attribs)
_add_common_attribs()

class _Entity(object):
    def __init__(self, **kwargs):
        self.attribs = {}
        self['layer'] = '0' # set default layer
        # set attribs from kwargs
        for key, value in kwargs.items():
            # linetype can be None which means BYLAYER!
            # and BYLAYER is defined as linetype is omitted
            if value is not None:
                self[key] = value

    @property
    def attribute_definition(self):
        """ get its own attribute definitions """
        return _DXF12_EntityAttributeDefinition[self.name]

    @property
    def name(self):
        """ key to attribute definitions, example: 'CIRCLE' """
        return 'ABSTRACT'

    def is_valid_attribute_name(self, key):
        """ True if an AttribDef for key exists. """
        return key in self.attribute_definition

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
        attrib = self.attribute_definition[attribname]
        return attrib.factory(value, attrib.group_code)

    def _priority(self, key):
        """ get priority of attribute key """
        return self.attribute_definition[key].priority

    def get_attribs(self):
        """ get attribs sorted by priority """
        priority_attribs = [ (self._priority(key), value)
                 for key, value in self.attribs.items() ]
        return [ value for priority, value  in sorted(priority_attribs) ]

    def get_data(self): # abstract
        # example: block->content, polyline->vertices, faces, insert->attribs
        return DXFList()

    def valid(self):
        """ validate object before dxf output """
        return True

    def extension_point(self): # abstract
        """ general extension point, first call in __dxf__.
        """
        pass

    def __dxf__(self):
        """ create the dxf string """
        self.extension_point() # last chance to manipulate the entity
        if self.valid():
            dxf = DXFList()
            dxf.append(DXFAtom(self.name))
            dxf.extend(self.get_attribs()) # attribs sorted by priority
            dxf.extend(self.get_data()) # example: block->content, polyline->vertices, faces, insert->attribs
            return dxfstr(dxf)
        else:
            raise DXFValidationError("invalid or missing attributs in object '%s'." % self.__class__.__name__)

class Line(_Entity):
    def __init__(self, **kwargs):
        default = {
            'start': (0,0),
            'end': (0,0),
        }
        default.update(kwargs)
        super(Line, self).__init__(**default)

    @property
    def name(self):
        return 'LINE'

class Point(_Entity):
    def __init__(self, **kwargs):
        default = {
            'point': (0,0),
        }
        default.update(kwargs)
        super(Point, self).__init__(**default)

    @property
    def name(self):
        return 'POINT'

class Solid(_Entity):
    def __init__(self, points=[], **kwargs):
        super(Solid, self).__init__(**kwargs)
        self.set_points(points)

    def set_points(self, points):
        for key, point in enumerate( points):
            self[key] = point

    @property
    def name(self):
        return 'SOLID'

    def extension_point(self):
        if 3 not in self.attribs:
            try:
                self[3] = self[2]['xyz'] # assign a tuple not a DXFPoint3D
            except KeyError: # validate fails at all
                pass

    def valid(self):
        for key in range(4):
            if key not in self.attribs:
                return False
        return True

class Trace(Solid):
    @property
    def name(self):
        return 'TRACE'

class Face3D(Solid):
    @property
    def name(self):
        return '3DFACE'

class Shape(_Entity):
    def __init__(self, **kwargs):
        default = {
            'insert': (0, 0),
            }
        default.update(kwargs)
        super(Shape, self).__init__(**default)

    @property
    def name(self):
        return 'SHAPE'

class Text(_Entity):
    def __init__(self, **kwargs):
        default = {
            'insert': (0, 0),
            'height': 1,
            'text': 'Text',
            }
        default.update(kwargs)
        super(Text, self).__init__(**default)

    @property
    def name(self):
        return 'TEXT'

class Arc(_Entity):
    def __init__(self, **kwargs):
        default = {
            'center': (0,0),
            'radius': 1,
            'startangle': 0,
            'endangle': 360,
        }
        default.update(kwargs)
        super(Arc, self).__init__(**default)

    @property
    def name(self):
        return 'ARC'

class Circle(_Entity):
    def __init__(self, **kwargs):
        default = {
            'center': (0,0),
            'radius': 1,
        }
        default.update(kwargs)
        super(Circle, self).__init__(**default)

    @property
    def name(self):
        return 'CIRCLE'

class Insert(_Entity):
    """ Insert a block reference, add attributes with add(attribute).

    The (Insert) attrib 'attribs_follow' is managed by the object itself, and
    a DXFAtom('SEQEND') will be added to end of the attibs list.
    """
    def __init__(self, **kwargs):
        default = {
            'insert': (0,0),
        }
        default.update(kwargs)
        super(Insert, self).__init__(**default)
        self.data = DXFList()

    @property
    def name(self):
        return 'INSERT'

    def add(self, attrib, relative=True):
        """ add attributes to a block reference. The position in attrib is
        absolute in WCS, or relative to the block origin (rotation is relative
        to the block x-axis).
        Angles are treated in degrees (circle=360 deg) in dxf-format.

        PARAMETER

        attrib
            the dxf attrib object

        relative
            Insert attrib relative to the block origin (0, 0, 0), this is perhaps
            not the insert point of the block!
            The relative position will be taken from the attrib.
        """
        def transform(insert_position, insert_rotation, delta):
            """ transforms x,y -> x',y' z-axis is ignored. """
            new_angle = math.radians(insert_rotation) + math.atan2(delta[1], delta[0])
            radius = math.hypot(delta[0], delta[1])
            dx = radius * math.cos(new_angle)
            dy = radius * math.sin(new_angle)
            return (insert_position[0]+dx, insert_position[1]+dy, insert_position[2])

        if relative is True:
            angel0 = DXFAngle(0.)
            relative_position = attrib['insert']['xyz']
            relative_angle = attrib.attribs.get('rotation', angel0).value
            insert_position = self['insert']['xyz']
            insert_angle = self.attribs.get('rotation', angel0).value
            insert_position = transform(insert_position, insert_angle, relative_position)
            # if block reference (insert-entity) is scaled in y-axis
            # then also shrink the textheight of the attrib-entity
            if 'yscale' in self.attribs:
                text_height = attrib['height']
                attrib['height'] = text_height * self['yscale']
            attrib['insert'] = insert_position
            # align point is always the insert point, so baseline styles
            # like ALIGNED, FIT and BASELINE_MIDDLE is not available
            attrib['alignpoint'] = insert_position
            attrib['rotation'] = insert_angle + relative_angle
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

    @property
    def name(self):
        return 'ATTDEF'

    def new_attrib(self, **kwargs):
        """ Create a new ATTRIB with attdef's attributs as default values.

        :param kwargs: override the attdef default values.

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

    @property
    def name(self):
        return 'ATTRIB'

class Block(_Entity):
    def __init__(self, **kwargs):
        """ data has to have the __dxf__ interface and an append method. """
        default = {
            'name': 'empty',
            'flags': 0,
            'basepoint': (0,0),
        }
        default.update(kwargs)
        super(Block, self).__init__(**default)
        self.data = DXFList()

    def find_attdef(self, tag):
        for entity in iterflatlist(self.data): # flatten nested list
            if isinstance(entity, _Entity) and \
                (entity.name == 'ATTDEF') and \
                (entity['tag'] == tag):
                return entity
        raise KeyError("no attdef with tag '%s' found!" % str(tag))

    def add(self, entity):
        self.data.append(entity)

    def extension_point(self):
        self['name2'] = self['name']
        if not self.valid():
            self.data.extend(self.blockend())

    def blockend(self):
        return [DXFAtom('ENDBLK')]

    def valid(self):
        if len(self.data) == 0:
            return False
        else:
            return self.data.endswith('ENDBLK')

    def get_data(self):
        return self.data

    @property
    def name(self):
        return 'BLOCK'

class Polyline(_Entity):
    """ 3D polyline

    MEMBERS

    vertices
        list of vertices, has to have the __dxf__ interface and an append method

    PUBLIC METHODS

    add_vertex
        add one vertex
    add_vertices
        add a list of vertices
    close
        set close-status of polyline
    """
    def __init__(self, points=[], **kwargs):
        """ polyline constructor

        points
            list of points, 2D or 3D points, z-value of 2D points is 0.
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

    @property
    def name(self):
        return 'POLYLINE'

    def close(self, status=True):
        """ closed polyline: first vertex is connected with last vertex.

        status
            True: polyline is closed
            False: polyline is open
        """
        self['flags'] = set_flag(self['flags'], const.POLYLINE_CLOSED, status)

    def add_vertex(self, point, **kwargs):
        """ point is a 2D or 3D point, z-value of a 2D point is 0. """
        self.vertices.append(Vertex(location=point, **kwargs))

    def add_vertices(self, points):
        """ add multiple points """
        for point in points:
            self.add_vertex(point)

    def extension_point(self):
        """ check before output """
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
    """ m(rows) x n(cols) polymesh, each col has m vertices and eachs row has n
    vertices.

    indices for a 3 x 2 mesh = (0,0)(0,1)|(1,0)(1,1)|(2,0)(2,1)

    PUBLIC METHODS

    set_mclosed(status)
        set close-status of m-direction, if status is True mesh is closed in m-dir
    set_nclosed(status)
        set close-status of n-direction, if status is True mesh is closed in n-dir
    set_vertex(row, col, point)
        set vertex at pos(row, col) to point, point is a 2D or 3D point
        z-value of 2D points is 0.
    """
    def __init__(self, nrows, ncols, **kwargs):
        """ 2 <= nrows <= 256; 2 <= ncols <= 256
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
    @property
    def name(self):
        return 'POLYLINE' # a polymesh is also a polyline

    def _build_vertex(self, point):
        return Vertex(location=point, flags=const.VTX_3D_POLYGON_MESH_VERTEX)

    def set_vertex(self, row, col, point):
        """ row and col are zero-based indices, point is a tuple (x,y,z)
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
    """ freeform polymesh with arbitrary count of faces.

    PUBLIC METHODS

    add_face(vertices, color)
        add a face with 3 ot 4 points, if points are 2D, z-value is 0.
    """
    def __init__(self, precision=6, **kwargs):
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

    @property
    def name(self):
        return 'POLYLINE' # a polyface is also a polyline

    def _build_vertex(self, point):
        return Vertex(location=point,
                      flags=const.VTX_3D_POLYGON_MESH_VERTEX + \
                      const.VTX_3D_POLYFACE_MESH_VERTEX)

    def _build_face(self, color):
        return Vertex(flags=const.VTX_3D_POLYFACE_MESH_VERTEX, color=color)
    # do not delete 'location' for the face-vertex, it is needed,
    # even though it is always (0,0,0), tested with AutoCAD

    def add_face(self, vertices, color=0):
        """ vertices is a list or tuple with 3 or 4 points (x,y,z).

        This is the recommend method for adding faces.
        """
        # len-check prevents usage of generators!
        # if len(vertices) not in (3, 4): raise ValueError
        self.add_face_by_indices(
            (self.add_vertex(point) for point in vertices),
            color)

    def add_vertex(self, point):
        """ add point to vertices and return the index of the vertex.
        """
        def key(point):
            """ vertex key with reduced floating point precision, near points
            will reference the same vertex. This reduces the vertices count, but
            it also reduces the accuracy of the model, use this wisly. You can
            control the function by the parameter self.precision, which determines
            the floting point precision.

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
        """ indices is a list or tuple of vertex indices (got from add_vertex). """
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
    def __init__(self, **kwargs):
        default = {
            'location': (0, 0, 0),
        }
        default.update(kwargs)
        super(Vertex, self).__init__(**default)

    @property
    def name(self):
        return 'VERTEX'
