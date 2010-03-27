#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: utility functions
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import math

HALF_PI = math.pi / 2.
THREE_PI_HALF = 1.5 * math.pi
DOUBLE_PI = math.pi * 2.

def truecolor(color_tuple=(0, 0, 0)):
    red, green, blue = color_tuple
    return ((red&255) << 16) + ((green&255) << 8) + (blue&255)

def int2hex(value):
    return hex(value)[2:].upper()

def hex2int(string):
    return int(string, 16)

def set_flag(value, bitmask, switch_on=True):
    if switch_on:
        return value | bitmask
    else:
        return value & ~bitmask

def flatten(alist):
    result = []
    for element in alist:
        if hasattr(element, "__iter__") and not isinstance(element, basestring):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result

def iterflatlist(alist):
    for element in alist:
        if hasattr(element, "__iter__") and not isinstance(element, basestring):
            for item in iterflatlist(element):
                yield item
        else:
            yield element

def rotate_2d(point, angle):
    """ rotate point around origin point about angle """
    x = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    y = point[1] * math.cos(angle) + point[0] * math.sin(angle)
    return (x, y)

def equals_almost(v1, v2, places=7):
    """compare two float values
       places: significant decimal places
    """
    return round(v1, places) == round(v2, places)

def normalize_angle(angle):
    """ return an angle between 0 and 2*pi """
    angle = math.fmod(angle, DOUBLE_PI)
    if angle < 0:
        angle += DOUBLE_PI
    return angle

def is_vertical_angle(angle, places=7):
    """ returns True for 1/2pi and 3/2pi """
    angle = normalize_angle(angle)
    return (equals_almost(angle, HALF_PI, places) or
            equals_almost(angle, THREE_PI_HALF, places))

def get_angle(p1, p2):
    """calc angle between the line p1-p2 and the x-axis
    input: points as tuples
    result: angle in radians
    """
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.atan2(dy, dx)

def distance(p1, p2):
    """calc distance between p1 and p2
    """
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    try:
        dz = p1[2] - p2[2]
    except IndexError:
        dz = 0.
    return (dx**2 + dy**2 + dz**2) ** .5

def midpoint(p1, p2):
        """ calculates the middle point between p1 and p2
        input: point as Point2D
        return: Point2D
        """
        x = (p1[0] + p2[0]) / 2.0
        y = (p1[1] + p2[1]) / 2.0
        try:
            z = (p1[2] + p2[2]) / 2.0
        except IndexError:
            z = 0.
        return (x, y, z)

def right_of_line(point, p1, p2):
    """ True if the point self is right of the line p1 -> p2
    """
    return not left_of_line(point, p1, p2)

def left_of_line(point, p1, p2):
    """ True if the point self is left of the line p1 -> p2
    """
    # check if a and b are on the same vertical line
    if p1[0] == p2[0]:
        # compute # on which site of the line self should be
        should_be_left = p1[1] < p2[1]
        if should_be_left:
            return point[0] < p1[0]
        else:
            return point[0] > p1[0]
    else:
        # get pitch of line
        pitch = (p2[1] - p1[1]) / (p2[0] - p1[0])

        # get y-value at c's x-position
        y = pitch * (point[0] - p1[0]) + p1[1]

        # compute if point should be above or below the line
        should_be_above = p1[0] < p2[0]
        if should_be_above :
            return point[1] > y
        else:
            return point[1] < y

def magnitude(vector):
    """ get magnitude (length) of vector """
    return sum([x**2 for x in vector ]) ** .5

def unit_vector(vector):
    """ get unit-vector of 3D vector (magnitude = 1.0) """
    m = magnitude(vector)
    return(vector[0]/m, vector[1]/m, vector[2]/m)

# dxfwrite should be independent from numpy!
def dot_product(vector1, vector2):
    """ get dot-product for vectors """
    return reduce(lambda x,y: x+y,
                  (a * b for a, b in zip(vector1, vector2)))

# dxfwrite should be independent from numpy!
def cross_product(vector1, vector2):
    """ get cross-product for 3D vectors """
    a1, a2, a3 = vector1
    b1, b2, b3 = vector2
    return (a2*b3-a3*b2, a3*b1-a1*b3, a1*b2-a2*b1)

_LIMIT = 1./64.
_WY = (0., 1., 0.)
_WZ = (0., 0., 1.)

def get_OCS(zvector):
    """Get the Object-Coordinate-System (a.k.a. ECS Entity-C-S).

    The arbitrary axis algorithm is used by AutoCAD internally to implement
    the arbitrary but consistent generation of object coordinate systems for all
    entities which use object coordinates.
    """
    az = unit_vector(zvector)
    if (abs(az[0]) < _LIMIT) and (abs(az[1]) < _LIMIT):
        ax = unit_vector(cross_product(_WY, az))
    else:
        ax = unit_vector(cross_product(_WZ, az))
    ay = unit_vector(cross_product(az, ax))
    return (ax, ay, az) # 3 unit-vectors!
