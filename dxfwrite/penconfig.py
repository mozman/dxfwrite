#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: read, create and write acad ctb files
# Created: 23.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from cStringIO import StringIO
from struct import pack
import zlib

ENDSTYLE_BUTT = 0
ENDSTYLE_SQUARE = 1
ENDSTYLE_ROUND = 2
ENDSTYLE_DIAMOND = 3
ENDSTYLE_OBJECT = 4


JOINSTYLE_MITER = 0
JOINSTYLE_BEVEL = 1
JOINSTYLE_ROUND = 2
JOINSTYLE_DIAMOND = 3
JOINSTYLE_OBJECT = 4

FILL_STYLE_SOLID = 64
FILL_STYLE_CHECKERBOARD = 65
FILL_STYLE_CROSSHATCH =66
FILL_STYLE_DIAMONDS = 67
FILL_STYLE_HORIZONTAL_BARS = 68
FILL_STYLE_SLANT_LEFT = 69
FILL_STYLE_SLANT_RIGHT = 70
FILL_STYLE_SQUARE_DOTS = 71
FILL_STYLE_VERICAL_BARS = 72
FILL_STYLE_OBJECT = 73

# add to switch both on: DITHERING_ON + GRAYSCALE_ON
DITHERING_ON = 1 # bit coded color_policy
GRAYSCALE_ON = 2 # bit coded color_policy

AUTOMATIC = 0
OBJECT_LINEWEIGHT = 0

OBJECT_COLOR = -1
OBJECT_COLOR2 = -1006632961

DEFAULT_LINE_WEIGHTS = [
 0.00, # 0
 0.05, # 1
 0.09, # 2
 0.10, # 3
 0.13, # 4
 0.15, # 5
 0.18, # 6
 0.20, # 7
 0.25, # 8
 0.30, # 9
 0.35, # 10
 0.40, # 11
 0.45, # 12
 0.50, # 13
 0.53, # 14
 0.60, # 15
 0.65, # 16
 0.70, # 17
 0.80, # 18
 0.90, # 19
 1.00, # 20
 1.06, # 21
 1.20, # 22
 1.40, # 23
 1.58, # 24
 2.00, # 25
 2.11, # 26
]

def color_name(index):
    return 'Color_{0}'.format(index+1)

class Pen(object):
    def __init__(self, index, init_dict={}):
        self.index = index
        self.name = unicode(init_dict.get('name', color_name(index)))
        self.localized_name = self.name
        self.description = unicode(init_dict.get('description', ""))
        self._color = int(init_dict.get('color', OBJECT_COLOR))
        if self._color != OBJECT_COLOR:
            self._mode_color = int(init_dict.get('mode_color', OBJECT_COLOR2))
        self.color_policy = int(init_dict.get('color_policy', DITHERING_ON))
        self.physical_pen_number = int(init_dict.get('pysical_pen_number', AUTOMATIC))
        self.virtual_pen_number = int(init_dict.get('virtual_pen_number', AUTOMATIC))
        self.screen = int(init_dict.get('screen', 100))
        self.linepattern_size = float(init_dict.get('linepattern_size', 0.5))
        self.linetype = int(init_dict.get('linetype', 31)) # 0 .. 30
        self.adaptive_linetype = init_dict.get('adaptive_line', 'TRUE') == 'TRUE'
        self.lineweight = int(init_dict.get('lineweight', OBJECT_LINEWEIGHT))
        self.end_style = int(init_dict.get('end_style', ENDSTYLE_OBJECT))
        self.join_style = int(init_dict.get('join_style', JOINSTYLE_OBJECT))
        self.fill_style = int(init_dict.get('fill_style', 73))

    @staticmethod
    def default_style(index):
        pen = Pen(index)
        pen._color = -1 # object color
        return pen

    def set_color(self, red, green, blue):
        self._color = mode_color2int(red, green, blue)
        self._mode_color = self._color

    def set_object_color(self):
        self._color = OBJECT_COLOR
        self._mode_color = OBJECT_COLOR

    def has_object_color(self):
        return self._color == -1 or self._color==OBJECT_COLOR

    def get_color(self):
        if self.has_object_color():
            return None # object color
        else:
            return int2color(self._mode_color)[:3]

    def write(self, fp):
        """Write pen data to file <fp>."""
        fp.write(' {0}{{\n'.format(self.index))
        fp.write('  name="{0}\n'.format(self.name))
        fp.write('  localized_name="{0}\n'.format(self.localized_name))
        fp.write('  description="{0}\n'.format(self.description))
        fp.write('  color={0}\n'.format(self._color))
        if self._color != -1:
            fp.write('  mode_color={0}\n'.format(self._mode_color))
        fp.write('  color_policy={0}\n'.format(self.color_policy))
        fp.write('  physical_pen_number={0}\n'.format(self.physical_pen_number))
        fp.write('  virtual_pen_number={0}\n'.format(self.virtual_pen_number))
        fp.write('  screen={0}\n'.format(self.screen))
        fp.write('  linepattern_size={0}\n'.format(self.linepattern_size))
        fp.write('  linetype={0}\n'.format(self.linetype))
        fp.write('  adaptive_linetype={0}\n'.format(unicode(bool(self.adaptive_linetype)).upper()))
        fp.write('  lineweight={0}\n'.format(self.lineweight))
        fp.write('  fill_style={0}\n'.format(self.fill_style))
        fp.write('  end_style={0}\n'.format(self.end_style))
        fp.write('  join_style={0}\n'.format(self.join_style))
        fp.write(' }\n')

class PenStyles(object, ):
    def __init__(self):
        self.description = ""
        self.write_aci_table = False
        self.scale_factor = 1.0
        self.apply_factor = False
        self.custom_lineweight_display_units = 0
        self.styles = {}
        self.lineweights = list(DEFAULT_LINE_WEIGHTS)

    def new(self, index, init_dict={}):
        pen = Pen(index, init_dict)
        self.styles[pen.name] = pen
        return pen

    def get(self, name):
        return self.styles[name]

    def get_style_number(self, index):
        for style in self.styles.itervalues():
            if index == style.index:
                return style
        return None

    def set_lineweight(self, index, weight):
        try:
            self.lineweights[index] = weight
            return index
        except IndexError:
            self.lineweights.append(weight)
            return len(self.lineweights)-1

    def get_lineweight(self, index):
        return self.lineweights[index]

    def write(self, fp):
        memfile=StringIO()
        self.write_content(memfile)
        memfile.write(chr(0)) # end of file
        body = memfile.getvalue()
        memfile.close()
        self._compress(fp, body)

    def write_content(self, fp):
        self._write_header(fp)
        if self.write_aci_table:
            self._write_aci_table(fp)
        self._write_ctb_plot_styles(fp)
        self._write_lineweights(fp)

    def _write_header(self, fp):
        fp.write('description="{0}\n'.format(self.description))
        write_aci = unicode(self.write_aci_table).upper()
        fp.write('aci_table_available={0}\n'.format(write_aci))
        fp.write('scale_factor={0:.1f}\n'.format(self.scale_factor))
        fp.write('apply_factor={0}\n'.format(unicode(self.apply_factor).upper()))
        fp.write('custom_lineweight_display_units={0}\n'.format(
            self.custom_lineweight_display_units))

    def _write_aci_table(self, fp):
        fp.write('aci_table{\n')
        for index in xrange(255):
            style = self.get_style_number(index)
            fp.write(' {0}="{1}\n'.format(index, style.name))
        fp.write('}\n')

    def _write_ctb_plot_styles(self, fp):
        fp.write('plot_style{\n')
        for index in xrange(255):
            style = self.get_style_number(index)
            if style is None:
                style = Pen.default_style(index)
            style.write(fp)
        fp.write('}\n')

    def _write_lineweights(self, fp):
        fp.write('custom_lineweight_table{\n')
        for index, weight in enumerate(self.lineweights):
            fp.write(' {0}={1}\n'.format(index, weight))
        fp.write('}\n')

    def parse(self, text):
        def set_lineweights(lineweights):
            if len(lineweights)> len(self.lineweights):
                self.lineweights = [0.0] * len(lineweights)
            for key, value in lineweights:
                self.lineweights[int(key)] = float(value)

        parser = CtbParser(text)
        self.description = parser.get('description', "")
        self.write_aci_table = parser.get('aci_table_available', 'FALSE').upper() == 'TRUE'
        self.scale_factor = float(parser.get('scale_factor', 1.0))
        self.apply_factor = (parser.get('apply_factor', 1.0).upper() == 'TRUE')
        self.custom_lineweight_display_units = int(
            parser.get('custom_lineweight_display_units', 1.0))
        set_lineweights = parser.get('custom_lineweight_table', None)
        styles = parser.get('plot_style', None)
        for index, style in styles.iteritems():
            pen = Pen(index, style)
            self.styles[pen.name] = pen

    def _compress(self, fp, body):
        header = 'PIAFILEVERSION_2.0,CTBVER1,compress\r\npmzlibcodec'
        fp.write(header)
        full_len = len(body)
        comp_body = zlib.compress(body)
        comp_len = len(comp_body)
        adler = zlib.adler32(comp_body)
        fp.write(pack('LLL', adler, full_len, comp_len))
        fp.write(comp_body)

def read(fp):
    content = _decompress(fp)
    styles = PenStyles()
    styles.parse(content)
    return styles

def _decompress(fp):
    content = fp.read()
    text = zlib.decompress(content[60:])
    return text[:-1] # truncate trailing \nul


class CtbParser(object):
    def __init__(self, text):
        self.data = {}
        for element, value in self.iter_elements(text):
            self.data[element] = value

    def iter_elements(self, text):
        def get_name(num):
            line = lines[num]
            if line.endswith('{'):
                name = line[:-1]
            else:
                name = line.split('=', 1)[0]
            return name.strip()

        def get_list(num):
            data = dict()
            while not lines[num].endswith('}'):
                name = get_name(num)
                num, value = get_value(num)
                data[name] = value
            return num+1, data

        def get_value(num):
            line=lines[num]
            if line.endswith('{'):
                num, value = get_list(num+1)
            else:
                value = line.split('=', 1)[1]
                value = value.lstrip('"')
                num = num + 1
            return num, value

        def skip_empty_lines(num):
            while num < len(lines) and len(lines[num]) == 0:
                num += 1
            return num

        lines = text.split('\n')
        num = 0
        while num < len(lines):
            name = get_name(num)
            num, value = get_value(num)
            yield(name, value)
            num = skip_empty_lines(num)

    def get(self, name, default):
        return self.data.get(name, default)

def int2color(color):
    magic = (color & 0xff000000) >> 24
    red = (color & 0xff0000) >> 16
    green = (color & 0xff00) >> 8
    blue = color & 0xff
    return (red, green, blue, magic)

def mode_color2int(red, green, blue, magic=0xc2):
    return -color2int(red, green, blue, magic)

def color2int(red, green, blue, magic):
    return -((magic << 24) + (red << 16) + (green << 8) + blue) & 0xffffffff

if __name__ == "__main__":
    # filename = r'D:\User\Python\ctb\acad2.stb'
    ctb = PenStyles()
    for index in xrange(75):
        ctb.new(index, {'linetype': index})

    with open(r'D:\User\Python\ctb\test.ctb', 'wb') as fp:
        ctb.write(fp)

