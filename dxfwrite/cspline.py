#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: 2d spline
# module belongs to package: cadlib.py
# Created: 26.03.2010
# License: GPL
# Source: http://www-lehre.informatik.uni-osnabrueck.de/~cg/2000/skript/7_2_Splines.html

import math
from array import array

def _coords(points, index=0):
    return array('f' , (point[index] for point in points))

class CubicSpline(object):
    def __init__(self, points):
        self.breakpoints = points
        self.t = self.get_t_array(points)

    @property
    def count(self):
        return len(self.breakpoints)

    def create_array(self):
        return array('f', (0.0 for i in xrange(self.count)))

    def get_t_array(self, points):
        t = array('f')
        t.append(0.0)
        for p1, p2 in zip(points[:-1], points[1:]):
            distance = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
            t.append(t[-1] + distance)
        return t

    def approximate(self, count):
        return zip(self.cubic_spline(_coords(self.breakpoints, 0), count),
                   self.cubic_spline(_coords(self.breakpoints, 1), count))

    def cubic_spline(self, f, spline_size):
        def get_delta_t_D(f):
            delta_t = self.create_array()
            D = self.create_array()
            for i in nrange:
                delta_t[i] = t[i] - t[i-1];
                D[i] = (f[i] - f[i-1])/ delta_t[i]
            delta_t[0] = t[2] - t[0]
            return delta_t, D

        def get_b_c(a, D, delta_t):
            b = self.create_array()
            c = self.create_array()
            for i in nrange[1:]:
                dh = D[i]
                bh = delta_t[i]
                e = a[i-1] + a[i] - 2. * dh
                b[i-1] = 2. * (dh - a[i-1] - e) / bh
                c[i-1] = 6. * e / (bh * bh)
            return b, c

        def get_a(h, k, m, delta_t):
            a = self.create_array()
            a[n-1] = (h * k[n-2] + k[n-1]) / m[n-1]
            for i in reversed(nrange[:-1]):
                a[i] = (k[i] - delta_t[i] * a[i+1]) / m[i]
            return a

        def get_h_k_m(D, delta_t):
            m = self.create_array()
            k = self.create_array()
            h = delta_t[1]
            m[0] = delta_t[2]
            k[0] = ((h + 2 * delta_t[0]) * D[1] * delta_t[2] + h * h * D[2]) / delta_t[0]
            for i in nrange[1:-1]:
                h = -delta_t[i+1] / m[i-1]
                k[i] = h * k[i-1] + 3 * (delta_t[i] * D[i+1] + delta_t[i+1] * D[i])
                m[i] = h * delta_t[i-1] + 2 * (delta_t[i] + delta_t[i+1])

            h = t[n-1] - t[n-3]
            dh = delta_t[n-1]
            k[n-1] = ((dh + h + h) * D[n-1] * delta_t[n-2] + dh * dh * D[n-2]) / h
            h = -h / m[n-2]
            m[n-1] = (h + 1.) * delta_t[n-2]
            return h, k, m

        n = self.count
        t = self.t
        nrange = range(n)

        delta_t, D = get_delta_t_D(f)
        h, k, m = get_h_k_m(D, delta_t)
        a = get_a(h, k, m, delta_t)
        b, c = get_b_c(a, D, delta_t)

        wt = 0.0
        j = 0
        dt = t[n-1] / float(spline_size - 1)
        for i in range(spline_size-1):
            while (j < (n-1)) and (t[j+1] < wt):
                j += 1
            h = wt - t[j]
            yield f[j] + h * (a[j] + h * (b[j] + h * c[j] / 3.) / 2.)
            wt = wt + dt
        yield f[n-1]
