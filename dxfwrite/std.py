#!/usr/bin/env python
#coding:utf-8
# Purpose: standard data and definitions
# module belongs to package: dxfwrite.py
# Created: 09.02.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

__author__ = "mozman <mozman@gmx.at>"

from array import array

from .htmlcolors import get_color_tuple_by_name

# dxf default pen assignment:
# 1 : 1.40mm - red
# 2 : 0.35mm - yellow
# 3 : 0.70mm - green
# 4 : 0.50mm - cyan
# 5 : 0.13mm - blue
# 6 : 1.00mm - magenta
# 7 : 0.25mm - white/black
# 8, 9 : 2.00mm
# >=10 : 1.40mm

# iso/din default pen assignment:
# 1 : 0.50mm - red/brown
# 2 : 0.35mm - yellow
# 3 : 1.00mm - green
# 4 : 0.70mm - cyan
# 5 : 0.70mm - blue
# 6 : 0.18mm - magenta
# 7 : 0.25mm - white/black
# >=8 : 0.25

dxf_default_color_table = [  # [0] is a dummy value, valid dxf color index = [1..255]
    (0, 0, 0), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255),
    (255, 0, 255), (255, 255, 255), (65, 65, 65), (128, 128, 128), (255, 0, 0),
    (255, 170, 170), (189, 0, 0), (189, 126, 126), (129, 0, 0), (129, 86, 86),
    (104, 0, 0), (104, 69, 69), (79, 0, 0), (79, 53, 53), (255, 63, 0),
    (255, 191, 170), (189, 46, 0), (189, 141, 126), (129, 31, 0), (129, 96, 86),
    (104, 25, 0), (104, 78, 69), (79, 19, 0), (79, 59, 53), (255, 127, 0),
    (255, 212, 170), (189, 94, 0), (189, 157, 126), (129, 64, 0), (129, 107, 86),
    (104, 52, 0), (104, 86, 69), (79, 39, 0), (79, 66, 53), (255, 191, 0),
    (255, 234, 170), (189, 141, 0), (189, 173, 126), (129, 96, 0), (129, 118, 86),
    (104, 78, 0), (104, 95, 69), (79, 59, 0), (79, 73, 53), (255, 255, 0),
    (255, 255, 170), (189, 189, 0), (189, 189, 126), (129, 129, 0), (129, 129, 86),
    (104, 104, 0), (104, 104, 69), (79, 79, 0), (79, 79, 53), (191, 255, 0),
    (234, 255, 170), (141, 189, 0), (173, 189, 126), (96, 129, 0), (118, 129, 86),
    (78, 104, 0), (95, 104, 69), (59, 79, 0), (73, 79, 53), (127, 255, 0),
    (212, 255, 170), (94, 189, 0), (157, 189, 126), (64, 129, 0), (107, 129, 86),
    (52, 104, 0), (86, 104, 69), (39, 79, 0), (66, 79, 53), (63, 255, 0),
    (191, 255, 170), (46, 189, 0), (141, 189, 126), (31, 129, 0), (96, 129, 86),
    (25, 104, 0), (78, 104, 69), (19, 79, 0), (59, 79, 53), (0, 255, 0),
    (170, 255, 170), (0, 189, 0), (126, 189, 126), (0, 129, 0), (86, 129, 86),
    (0, 104, 0), (69, 104, 69), (0, 79, 0), (53, 79, 53), (0, 255, 63),
    (170, 255, 191), (0, 189, 46), (126, 189, 141), (0, 129, 31), (86, 129, 96),
    (0, 104, 25), (69, 104, 78), (0, 79, 19), (53, 79, 59), (0, 255, 127),
    (170, 255, 212), (0, 189, 94), (126, 189, 157), (0, 129, 64), (86, 129, 107),
    (0, 104, 52), (69, 104, 86), (0, 79, 39), (53, 79, 66), (0, 255, 191),
    (170, 255, 234), (0, 189, 141), (126, 189, 173), (0, 129, 96), (86, 129, 118),
    (0, 104, 78), (69, 104, 95), (0, 79, 59), (53, 79, 73), (0, 255, 255),
    (170, 255, 255), (0, 189, 189), (126, 189, 189), (0, 129, 129), (86, 129, 129),
    (0, 104, 104), (69, 104, 104), (0, 79, 79), (53, 79, 79), (0, 191, 255),
    (170, 234, 255), (0, 141, 189), (126, 173, 189), (0, 96, 129), (86, 118, 129),
    (0, 78, 104), (69, 95, 104), (0, 59, 79), (53, 73, 79), (0, 127, 255),
    (170, 212, 255), (0, 94, 189), (126, 157, 189), (0, 64, 129), (86, 107, 129),
    (0, 52, 104), (69, 86, 104), (0, 39, 79), (53, 66, 79), (0, 63, 255),
    (170, 191, 255), (0, 46, 189), (126, 141, 189), (0, 31, 129), (86, 96, 129),
    (0, 25, 104), (69, 78, 104), (0, 19, 79), (53, 59, 79), (0, 0, 255),
    (170, 170, 255), (0, 0, 189), (126, 126, 189), (0, 0, 129), (86, 86, 129),
    (0, 0, 104), (69, 69, 104), (0, 0, 79), (53, 53, 79), (63, 0, 255),
    (191, 170, 255), (46, 0, 189), (141, 126, 189), (31, 0, 129), (96, 86, 129),
    (25, 0, 104), (78, 69, 104), (19, 0, 79), (59, 53, 79), (127, 0, 255),
    (212, 170, 255), (94, 0, 189), (157, 126, 189), (64, 0, 129), (107, 86, 129),
    (52, 0, 104), (86, 69, 104), (39, 0, 79), (66, 53, 79), (191, 0, 255),
    (234, 170, 255), (141, 0, 189), (173, 126, 189), (96, 0, 129), (118, 86, 129),
    (78, 0, 104), (95, 69, 104), (59, 0, 79), (73, 53, 79), (255, 0, 255),
    (255, 170, 255), (189, 0, 189), (189, 126, 189), (129, 0, 129), (129, 86, 129),
    (104, 0, 104), (104, 69, 104), (79, 0, 79), (79, 53, 79), (255, 0, 191),
    (255, 170, 234), (189, 0, 141), (189, 126, 173), (129, 0, 96), (129, 86, 118),
    (104, 0, 78), (104, 69, 95), (79, 0, 59), (79, 53, 73), (255, 0, 127),
    (255, 170, 212), (189, 0, 94), (189, 126, 157), (129, 0, 64), (129, 86, 107),
    (104, 0, 52), (104, 69, 86), (79, 0, 39), (79, 53, 66), (255, 0, 63),
    (255, 170, 191), (189, 0, 46), (189, 126, 141), (129, 0, 31), (129, 86, 96),
    (104, 0, 25), (104, 69, 78), (79, 0, 19), (79, 53, 59), (51, 51, 51),
    (80, 80, 80), (105, 105, 105), (130, 130, 130), (190, 190, 190), (255, 255, 255)]

# element [0] = default lineweight for undefined values
LW_DXF = [1.40, 1.40, 0.35, 0.70, 0.50, 0.13, 1.00, 0.25, 2.00, 2.00]
LW_ISO = [0.25, 0.50, 0.35, 1.00, 0.70, 0.70, 0.18, 0.25]
LW_DIN = LW_ISO


class DXFLineweight(object):

    def __init__(self, lineweights=LW_DXF, user_styles=None):
        self.set_defaults(lineweights)
        self.add_user_styles(user_styles)

    def set_defaults(self, lineweights):
        """Set default lineweights."""
        self.lineweights = array('f', [lineweights[0]]*256)
        for index, lw in enumerate(lineweights):
            self.lineweights[index] = lw

    def add_user_styles(self, user_styles):
        """Add all in <user_styles> defined lineweights."""
        if user_styles is None:
            return
        for dxf_index in range(1, 256):
            lw = user_styles.get_lineweight(dxf_index)
            if lw is not None:
                self.lineweights[dxf_index] = lw

    def get(self, dxf_color_index):
        """Get 'real' lineweight for <dxf_color_index> in mm."""
        if 0 < dxf_color_index < 256:
            return self.lineweights[dxf_color_index]
        else:
            raise IndexError('Index out of range.')

RED = 0
GREEN = 1
BLUE = 2


class DXFColorIndex(object):
    def __init__(self, color_table=dxf_default_color_table, user_styles=None,
                 start_index=1):
        # _color_table[0] is a dummy element, valid dxf index is in the range [1..255]
        # because of special meaning of color indices 0=BYBLOCK, 256=BYLAYER
        self.color_table = color_table[:]
        self.color_map = self.generate_color_map(self.color_table)
        self.start_index = start_index  # first dxf color element[0] is a dummy value
        if user_styles is not None:
            self.add_user_styles(user_styles)

    @staticmethod
    def generate_color_map(color_table):
        def iter_colors_backwards():
            lastindex = len(color_table) - 1
            for index, color in enumerate(reversed(color_table)):
                yield (lastindex - index, color)

        color_map = dict(iter_colors_backwards())
        if 0 in color_map:  # index 0 means BYBLOCK
            del color_map[0]
        return color_map

    def add_user_styles(self, pen_styles):
        """Add user styles to color_table and color_map.

        pen_styles -- requires a method <get_color(dxf_color_index)>, which
            returns for each dxf index a rgb-tuple or None if not defined
            see also dxfwrite.acadctb.PenStyles object
        """
        for dxf_color_index in range(self.start_index, len(self.color_table)):
            user_color = pen_styles.get_color(dxf_color_index)
            if user_color is not None:
                self.color_table[dxf_color_index] = user_color
        self.color_map = self.generate_color_map(self.color_table)

    def get_rgb(self, index):
        if self.start_index <= index < len(self.color_table):
            return self.color_table[index]
        else:
            raise IndexError('Index out of range.')

    def get_dxf_color_index(self, rgb):
        """ Get dxf_color_index of color with the nearest rgb-values.

        rgb -- (red, green , blue) values in range [0..255]
        """

        def get_color_distance(color1, color2):
            """ approximation for euclidean color distance for CIE XYZ color space
            """
            rmean = (float(color1[RED]) + float(color2[RED])) / 2.0
            delta_sqr = []
            for index in (RED, GREEN, BLUE):
                delta_sqr.append( (float(color1[index]) - float(color2[index]))**2 )
            part1 = (2. + rmean / 256.) * delta_sqr[RED]
            part2 = 4. * delta_sqr[GREEN]
            part3 = (2. + (255. - rmean)/256.) * delta_sqr[BLUE]
            return (part1 + part2 + part3) ** 0.5

        def nearest_color_index():
            min_distance = 100000.
            min_index = -1
            index = self.start_index
            max_index = len(self.color_table)
            while index < max_index:
                color = self.color_table[index]
                color_distance = get_color_distance(rgb, color)
                if color_distance < min_distance:
                    min_distance = color_distance
                    min_index = index
                index += 1
            return min_index

        # stupid special case black/white == 7
        # do not redefine color 7 with user values!!!
        if rgb == (0, 0, 0):
            return 7
        try:
            return self.color_map[rgb]
        except KeyError:
            return nearest_color_index()

    def get_dxf_color_index_by_colorname(self, colorname):
        colortuple = get_color_tuple_by_name(colorname)
        return self.get_dxf_color_index(colortuple)


def linetypes():
    """ Creates a list of standard line types.
    """
    # dxf linetype definition
    # name, description, elements:
    # elements = [total_pattern_length, elem1, elem2, ...]
    # total_pattern_length = sum(abs(elem))
    # elem > 0 is line, < 0 is gap, 0.0 = dot;
    return [("CONTINUOUS", "Solid", [0.0]),
            ("CENTER", "Center ____ _ ____ _ ____ _ ____ _ ____ _ ____",
             [2.0, 1.25, -0.25, 0.25, -0.25]),
            ("CENTERX2", "Center (2x) ________  __  ________  __  ________",
             [3.5, 2.5, -0.25, 0.5, -0.25]),
            ("CENTER2", "Center (.5x) ____ _ ____ _ ____ _ ____ _ ____",
             [1.0, 0.625, -0.125, 0.125, -0.125]),
            ("DASHED", "Dashed __ __ __ __ __ __ __ __ __ __ __ __ __ _",
             [0.6, 0.5, -0.1]),
            ("DASHEDX2", "Dashed (2x) ____  ____  ____  ____  ____  ____",
             [1.2, 1.0, -0.2]),
            ("DASHED2", "Dashed (.5x) _ _ _ _ _ _ _ _ _ _ _ _ _ _",
             [0.3, 0.25, -0.05]),
            ("PHANTOM", "Phantom ______  __  __  ______  __  __  ______",
             [2.5, 1.25, -0.25, 0.25, -0.25, 0.25, -0.25]),
            ("PHANTOMX2", "Phantom (2x)____________    ____    ____    ____________",
             [4.25, 2.5, -0.25, 0.5, -0.25, 0.5, -0.25]),
            ("PHANTOM2", "Phantom (.5x) ___ _ _ ___ _ _ ___ _ _ ___ _ _ ___",
             [1.25, 0.625, -0.125, 0.125, -0.125, 0.125, -0.125]),
            ("DASHDOT", "Dash dot __ . __ . __ . __ . __ . __ . __ . __",
             [1.4, 1.0, -0.2, 0.0, -0.2]),
            ("DASHDOTX2", "Dash dot (2x) ____  .  ____  .  ____  .  ____",
             [2.4, 2.0, -0.2, 0.0, -0.2]),
            ("DASHDOT2", "Dash dot (.5x) _ . _ . _ . _ . _ . _ . _ . _",
             [0.7, 0.5, -0.1, 0.0, -0.1]),
            ("DOT", "Dot .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .",
             [0.2, 0.0, -0.2]),
            ("DOTX2", "Dot (2x) .    .    .    .    .    .    .    . ",
             [0.4, 0.0, -0.4]),
            ("DOT2", "Dot (.5) . . . . . . . . . . . . . . . . . . . ",
             [0.1, 0.0, -0.1]),
            ("DIVIDE", "Divide __ . . __ . . __ . . __ . . __ . . __",
             [1.6, 1.0, -0.2, 0.0, -0.2, 0.0, -0.2]),
            ("DIVIDEX2", "Divide (2x) ____  . .  ____  . .  ____  . .  ____",
             [2.6, 2.0, -0.2, 0.0, -0.2, 0.0, -0.2]),
            ("DIVIDE2", "Divide(.5x) _ . _ . _ . _ . _ . _ . _ . _",
             [0.8, 0.5, -0.1, 0.0, -0.1, 0.0, -0.1]),
            ]


def styles():
    """ Creates a list of standard styles.
    """
    return [
        ('STANDARD', 'arial.ttf'),
        ('ARIAL', 'arial.ttf'),
        ('ARIAL_BOLD', 'arialbd.ttf'),
        ('ARIAL_ITALIC', 'ariali.ttf'),
        ('ARIAL_BOLD_ITALIC', 'arialbi.ttf'),
        ('ARIAL_BLACK', 'ariblk.ttf'),
        ('ISOCPEUR', 'isocpeur.ttf'),
        ('ISOCPEUR_ITALIC', 'isocpeui.ttf'),
        ('TIMES', 'times.ttf'),
        ('TIMES_BOLD', 'timesbd.ttf'),
        ('TIMES_ITALIC', 'timesi.ttf'),
        ('TIMES_BOLD_ITALIC', 'timesbi.ttf'),
    ]
