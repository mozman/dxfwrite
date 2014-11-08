#!/usr/bin/env python
# coding:utf-8
# Purpose: 2d vector math
# module belongs to package dxfwrite
# Created: 16.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License
"""
2d vector math module
"""

__author__ = "mozman <mozman@gmx.at>"

from math import hypot, atan2, sin, cos


def vector2d(vector):
    """ return a 2d vector """
    return (float(vector[0]), float(vector[1]))


def vector2angle(vector):
    """ get angle of vector """
    return atan2(vector[1], vector[0])


def angle2uv(angle):
    """ get unit_vector from angle """
    return (cos(angle), sin(angle))


def magnitude(vector):
    """ length of a 2d vector """
    return hypot(vector[0], vector[1])


def unit_vector(vector):
    """ 2d unit vector """
    return vdiv_scalar(vector, magnitude(vector))


def normal_vector(vector):
    """ 2d perpendicular vector """
    return (-vector[1], vector[0])


def distance(point1, point2):
    """ calc distance between two 2d points """
    return hypot(point1[0] - point2[0], point1[1] - point2[1])


def midpoint(point1, point2):
    """ calc midpoint between point1 and point2 """
    return ((point1[0] + point2[0]) * .5, (point1[1] + point2[1]) * .5)


def vsub(vector1, vector2):
    """ substract vectors """
    return (vector1[0] - vector2[0], vector1[1] - vector2[1])


def vadd(vector1, vector2):
    """ add vectors """
    return (vector1[0] + vector2[0], vector1[1] + vector2[1])


def vdiv_scalar(vector, scalar):
    """ div vectors """
    return (vector[0] / scalar, vector[1] / scalar)


def vmul_scalar(vector, scalar):
    """ mul vector with scalar """
    return (vector[0] * scalar, vector[1] * scalar)
