#!/usr/bin/env python
# coding:utf-8
# Created: 27.03.2010
# Purpose: 3d vectormath
# module belongs to package dxfwrite
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License
"""
3d vector math module
"""

__author__ = "mozman <mozman@gmx.at>"


def vector3d(vector):
    """ return a 3d vector """
    if len(vector) == 2:
        return float(vector[0]), float(vector[1]), 0.
    else:
        return float(vector[0]), float(vector[1]), float(vector[2])


def magnitude(vector):
    """ get magnitude (length) of vector """
    return (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** .5


def unit_vector(vector):
    """ get unit-vector of 3D vector (magnitude = 1.0) """
    m = magnitude(vector)
    return vector[0] / m, vector[1] / m, vector[2] / m


def dot_product(vector1, vector2):
    """ get dot-product for vectors """
    return reduce(lambda x, y: x + y,
                  (a * b for a, b in zip(vector1, vector2)))


def cross_product(vector1, vector2):
    """ get cross-product for 3D vectors """
    a1, a2, a3 = vector1
    b1, b2, b3 = vector2
    return a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1


def distance(point1, point2):
    """ calc distance between two 3d points """
    return ((point1[0] - point2[0]) ** 2 +
            (point1[1] - point2[1]) ** 2 +
            (point1[2] - point2[2]) ** 2) ** 0.5


def midpoint(point1, point2):
    """ calc midpoint between point1 and point2 """
    return ((point1[0] + point2[0]) * .5,
            (point1[1] + point2[1]) * .5,
            (point1[2] + point2[2]) * .5)
