#!/usr/bin/env python
# coding:utf-8
# Purpose: user coordinate system
# module belongs to package dxfwrite
# Created: 27.03.2010
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

import math

from .util import normal_vector, unit_vector, normalize_angle, get_angle

HALF_PI = math.pi / 2.


class UCS(object):
    def __init__(self, origin_vector=(0., 0., 0.),
                 xaxis_vector=(1., 0., 0.),
                 yaxis_vector=(0., 1., 0.)):
        self._xaxis = unit_vector(xaxis_vector)
        self._yaxis = unit_vector(yaxis_vector)
        self._zaxis = normal_vector(xaxis_vector, yaxis_vector)
        self._origin = origin_vector

    def to_world(self, ucsvector):
        return self._origin + \
               self._xaxis * ucsvector[0] + \
               self._yaxis * ucsvector[1] + \
               self._zaxis * ucsvector[2]

    def to_ucs(self, worldvector):
        v = worldvector - self._origin
        vx = v[0] / self._xaxis
        vy = v[1] / self._yaxis
        vz = v[2] / self._zaxis
        return vx + vy + vz

    def setup_xy(self, p1_world, p2_world, p1_ucs, p2_ucs):
        """ setup an UCS given by the points p1 and p2
        only xy-plane,  z' = z
        """
        ucs_angle_to_x_axis = get_angle(p1_ucs, p2_ucs)
        world_angle_to_x_axis = get_angle(p1_world, p2_world)
        rotation = normalize_angle(world_angle_to_x_axis - ucs_angle_to_x_axis)
        self._xaxis = (math.cos(rotation), math.sin(rotation), 0.)
        self._yaxis = (math.cos(rotation + HALF_PI), math.sin(rotation + HALF_PI), 0.)
        self._zaxis = (0., 0., 1.)

        ucs_angle_to_x_axis = get_angle((0., 0.), p1_ucs)
        world_angle_to_x_axis = rotation + ucs_angle_to_x_axis
        distance_from_ucs_origin = math.hypot(p1_ucs[0], p1_ucs[1])
        delta_x = distance_from_ucs_origin * math.cos(world_angle_to_x_axis)
        delta_y = distance_from_ucs_origin * math.sin(world_angle_to_x_axis)
        self._origin = (p1_world[0] - delta_x, p1_world[1] - delta_y, 0.)


class GKS(UCS):
    def to_world(self, ucs):
        """ get world coordinates for gauss krueger point
        """
        return super(GKS, self).to_world((ucs[1], ucs[0]))

    def to_ucs(self, world):
        """ get gauss krueger coordinates for world point
        """
        x, y, z = super(GKS, self).to_ucs(world)
        return (y, x, z)

    def setup_xy(self, p1_world, p2_world, p1_ucs, p2_ucs):
        """ create an GKS by the given points p1 and p2
        """
        p1_ucs = (p1_ucs[1], p1_ucs[0])
        p2_ucs = (p2_ucs[1], p2_ucs[0])
        super(GKS, self).setup_xy(p1_world, p2_world, p1_ucs, p2_ucs)

