#!/usr/bin/env python
#coding:utf-8
# Purpose: base types
# module belongs to package dxfwrite
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from .util import izip, PYTHON3, to_string, is_string, iterflatlist
if PYTHON3:
    xrange = range

from .vector3d import cross_product, unit_vector


def dxfstr(obj):
    """ Create the DXF string by calling the __dxf__() method.
    
    This method creates the strings as early as possible, which generates excessive 
    string concatenation.
    
    Returns a valid dxf-string, last char has to be '\n'.

    """
    return obj.__dxf__()


def iterdxftags(dxfobj):
    if hasattr(dxfobj, '__dxftags__'):
        for tag in dxfobj.__dxftags__():
            for subtag in iterdxftags(tag):
                    yield subtag
    else:
        yield dxfobj


def tags2str(dxfobj):
    """ Creates the DXF string by collecting the DXF tags at first, by iterating over all dxf tags.
    Creates the DXF string by only one ''.join() operation.
    
    This method creates the DXF string as late as possible.
    
    Returns a valid dxf-string, last char has to be '\n'.

    """
    return "".join( (tag.__dxf__() for tag in iterdxftags(dxfobj)) )


def writetags(fileobj, dxfobj, encoding=None):        
    if PYTHON3 or (encoding is None):
        write = lambda tag: fileobj.write(tag)
    else:
        write = lambda tag: fileobj.write(tag.encode(encoding))
        
    for dxftag in iterdxftags(dxfobj):
        write(dxftag.__dxf__())


class DXFValidationError(Exception):
    pass


class _DXFType(object):
    _group_code_types = None

    def __init__(self):
        if self._group_code_types is None:
            self._init_table()

    def _init_table(self):
        self._group_code_types = dict()
        for type_str, begin, end in [
            ('string', 0, 9),
            ('float', 10, 59),
            ('int', 60, 79),
            ('int', 90, 99),
            ('string', 100, 0),
            ('string', 102, 0),
            ('string', 105, 0),
            ('float', 110, 149),
            ('int', 170, 179),
            ('float', 210, 239),
            ('int', 270, 289),
            ('bool', 290, 299),
            ('string', 300, 369),
            ('int', 370, 389),
            ('string', 390, 399),
            ('int', 400, 409),
            ('string', 410, 419),
            ('int', 420, 429),
            ('string', 430, 439),
            ('int', 440, 459),
            ('float', 460, 469),
            ('string', 470, 479),
            ('string', 999, 1009),
            ('float', 1010, 1059),
            ('int', 1060, 1071),
            ]:
            self.add_group_code_type(type_str, begin, end)

    def check(self, value, code):
        try:
            typestr = self.group_code_type(code)
        except KeyError:
            raise ValueError("Unknown group code '%s'" % str(code))
        if typestr == 'string':
            return is_string(value)
        elif typestr == 'bool':
            return value in (0, 1)
        elif typestr == 'float':
            return isinstance(value, float)
        elif typestr == 'int':
            return isinstance(value, int)

    def cast(self, value, code):
        """ Convert value depending on group code """
        typestr = self.group_code_type(code)
        if typestr == 'string':
            return to_string(value)
        elif typestr == 'bool':
            return 1 if int(value) else 0
        elif typestr == 'float':
            return float(value)
        elif typestr == 'int':
            return int(value)
        raise ValueError("Unknown format '%s'" % to_string(code))

    def group_code_type(self, group_code):
        return self._group_code_types[group_code]

    def add_group_code_type(self, type_str, begin, end=0):
        if end <= begin:
            end = begin + 1
        else:
            end += 1

        for code in xrange(begin, end):
            self._group_code_types[code] = type_str


class DXFAtom(object):
    """ The basic dxf object """
    _dxftype = _DXFType()

    def __init__(self, value, group_code=0):
        self._group_code = int(group_code)
        self._value = self._typecast(value, self._group_code)

    def __dxf__(self):
        """ Returns a valid DXF String. Last char has to be '\n'. """
        return "%3d\n%s\n" % (self._group_code, to_string(self._value))

    def _typecast(self, value, group_code):
        return self._dxftype.cast(value, group_code)

    def is_3d_point_coord(self):
        return 10 <= self._group_code < 40

    def get_index_shift(self):
        """ returns the dxf-3d-point-value index (range = 0 .. 9).

        10, 20, 30 = index 0
        13, 23, 33 = index 3
        17, 27, 37 = index 7
        """
        if self.is_3d_point_coord():
            return int(self.group_code % 10)
        else:
            raise TypeError("Not a 3D point value")

    def get_axis_index(self):
        """ returns 0 for 'x', 1 for 'y' and 2 for 'z'.

        DXFPoint[axis_index]
        """
        if self.is_3d_point_coord():
            return int(self.group_code / 10) - 1
        else:
            raise TypeError("Not a 3D point value")

    @property
    def value(self): return self._value

    @property
    def group_code(self): return self._group_code

    def __eq__(self, atom):
        assert isinstance(atom, DXFAtom)
        return (self.group_code == atom.group_code) and \
               (self.value == atom.value)


class DXFList(list):
    """ Collection of DXFAtoms. """
    def __dxf__(self):
        """ Returns a valid DXF String. """
        return "".join((atom.__dxf__() for atom in self))

    def __dxftags__(self):
        return self

    def __eq__(self, dxflist):
        if len(self) != len(dxflist):
            return False
        for atom1, atom2 in izip(self, dxflist):
            if atom1 != atom2:
                return False
        return True

    def endswith(self, name):
        if len(self):
            try:
                if self[-1].value == name:
                    return True
            except AttributeError:
                pass
        return False


class DXFString(DXFAtom):
    """ String with group code 1 """
    def __init__(self, value, group_code=1):
        super(DXFString, self).__init__(to_string(value), group_code)


class DXFName(DXFAtom):
    """ String with group code 2 """
    def __init__(self, value, group_code=2):
        super(DXFName, self).__init__(to_string(value), group_code)


class DXFFloat(DXFAtom):
    """ float with group code 40 """
    def __init__(self, value, group_code=40):
        super(DXFFloat, self).__init__(float(value), group_code)


class DXFAngle(DXFAtom):
    """ float with group code 50, angle in degrees """
    def __init__(self, value, group_code=50):
        super(DXFAngle, self).__init__(float(value), group_code)


class DXFInt(DXFAtom):
    """ 16 bit integer with group code 70 """
    def __init__(self, value, group_code=70):
        super(DXFInt, self).__init__(int(value), group_code)


class DXFBool(DXFAtom):
    """ Integer 0 or 1 """
    def __init__(self, value=1, group_code=290):
        super(DXFBool, self).__init__(int(value), group_code)


class DXFPoint(object):
    """ 3D point with 3 float coordinates """
    def __init__(self, coords=(0., 0., 0.), index_shift=0):
        if len(coords) in (2, 3) :
            # just use a normal list not DXFList, because point has public access
            # and can be set as tuple or list too, so always expect a tuple or list
            self.point = [DXFFloat(value, (pos+1)*10+index_shift) for pos, value in enumerate(coords)]
        else:
            raise ValueError("only 2 or 3 coord-values allowed.")

    def __getitem__(self, axis):
        """ Get coordinate for 'axis'.

        PARAMETER
            axis: 0, 1, 2 or 'x', 'y', 'z'
            axis: 'xz' returns a list of 'x' and 'z' any combination of 'x', 'y'
            and 'z' is valid, ('xyz', 'zyx', 'xxy', 'xxxxx')
        """
        if axis in (0, 1, 2):
            try:
                return self.point[axis].value
            except IndexError:
                raise IndexError("DXF-Point has no '%s'-coordinate!" % ('x', 'y', 'z')[axis])
        elif is_string(axis):
            if axis in ('x', 'y', 'z'):
                try:
                    index = ord(axis) - ord('x')
                    return self.point[index].value
                except IndexError:
                    raise IndexError("DXF-Point has no '%s'-coordinate!" % axis)
            elif len(axis) > 1:  # 'xy' or 'zx' get coords in letter order
                return [self.__getitem__(index) for index in axis]
            else:
                raise IndexError("Invalid axis name '%s'" % axis)
        else:
            raise IndexError("Invalid axis name '%s'" % axis)

    def __dxf__(self):
        return "".join([coord.__dxf__() for coord in self.point])

    def get_index_shift(self):
        return self.point[0].group_code - 10

    def shift_group_code(self, index_shift):
        """ get DXFPoint with shifted group code """
        return DXFPoint(self["xyz"[:len(self.point)]], index_shift)

    def to_3D(self, zvalue=0.):
        """ add z-axis if absent """
        if len(self.point) < 3:
            self.point.append(DXFFloat(zvalue, self.get_index_shift()+30))

    @property
    def tuple(self):
        # CAUTION: do not override the 'value' attribute!!!
        # 'value' would be the suitable name for this property, but that causes
        # several serious problems.
        return tuple(self['xyz'[:len(self.point)]])


class DXFPoint2D(DXFPoint):
    """ only output x and y axis! """
    def __dxf__(self):
        return "".join([coord.__dxf__() for coord in self.point[:2]])


class DXFPoint3D(DXFPoint):
    """ An assurd 3D point """
    def __init__(self, coords=(0., 0., 0.), index_shift=0):
        if len(coords) == 2:
            coords = (coords[0], coords[1], 0.)
        super(DXFPoint3D, self).__init__(coords, index_shift)


def PassThroughFactory(value, group_code):
    return value


class AttribDef(object):
    """ Attribute definition

    ATTRIBUTES

    .. attribute:: group_code

        DXF group code

    .. attribute:: factory

        factory-function to create DXFAtoms, use PassThroughFactory for
        DXFList or list objects like DXFPoint or pattern in class Linetype().

    .. attribute:: priority

        determines the output order of attributes, not really necessary for
        the DXF-format (if you belief Autodesk), but useful for testing.
        Prints lower values before higher values. (50, 51, 52, 100, 101, 102)
    """
    def __init__(self, factory, group_code=0, priority=100):
        self.group_code = group_code
        self.factory = factory
        self.priority = priority

_LIMIT = 1./64.
_WY = (0., 1., 0.)
_WZ = (0., 0., 1.)


def get_OCS(zvector):
    """Get the Object-Coordinate-System (a.k.a. ECS Entity-C-S).

    The arbitrary axis algorithm is used by AutoCAD internally to implement
    the arbitrary but consistent generation of object coordinate systems for all
    entities which use object coordinates.

    untested!
    """
    az = unit_vector(zvector)
    if (abs(az[0]) < _LIMIT) and (abs(az[1]) < _LIMIT):
        ax = unit_vector(cross_product(_WY, az))
    else:
        ax = unit_vector(cross_product(_WZ, az))
    ay = unit_vector(cross_product(az, ax))
    return (ax, ay, az)  # 3 unit-vectors!
