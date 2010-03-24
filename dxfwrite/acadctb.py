#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: read, create and write acad ctb files
# Created: 23.03.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from cStringIO import StringIO
from array import array
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
JOINSTYLE_OBJECT = 5

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

STYLE_COUNT = 255

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
    """Define a pen style."""
    def __init__(self, index, init_dict={}):
        self.index = int(index)
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

    def set_color(self, red, green, blue):
        """Set color as rgb-tuple."""
        self._mode_color = mode_color2int(red, green, blue)
        # when defining a user-color, <mode_color> represents the real truecolor
        # as rgb-tuple with the magic number 0xC2 as highest byte, the <color>
        # value calculated for a user-color is not a rgb-tuple and has the magic
        # number 0xC3 (sometimes), I set for <color> the same value a for
        # <mode_color>, because Autocad corrects the <color> value by itself.
        self._color = self._mode_color

    def set_object_color(self):
        """Set color to object color."""
        self._color = OBJECT_COLOR
        self._mode_color = OBJECT_COLOR

    def has_object_color(self):
        """True if pen has object color."""
        return self._color == OBJECT_COLOR or \
               self._color == OBJECT_COLOR2

    def get_color(self):
        """Get pen color as rgb-tuple or None if pen has object color."""
        if self.has_object_color():
            return None # object color
        else:
            return int2color(self._mode_color)[:3]

    def get_dxf_color_index(self):
        return self.index+1

    @property
    def dithering(self):
        return bool(self.color_policy & DITHERING_ON)
    @dithering.setter # pylint: disable-msg=E1101
    def dithering(self, status): # pylint: disable-msg=E0102
        if status :
            self.color_policy |= DITHERING_ON
        else:
            self.color_policy &= ~DITHERING_ON

    @property
    def grayscale(self):
        return bool(self.color_policy & GRAYSCALE_ON)
    @grayscale.setter # pylint: disable-msg=E1101
    def grayscale(self, status): # pylint: disable-msg=E0102
        if status :
            self.color_policy |= GRAYSCALE_ON
        else:
            self.color_policy &= ~GRAYSCALE_ON

    def write(self, fp):
        """Write pen data to file-like object <fp>."""
        index = self.index
        fp.write(' {0}{{\n'.format(index))
        fp.write('  name="{0}\n'.format(color_name(index)))
        fp.write('  localized_name="{0}\n'.format(color_name(index)))
        fp.write('  description="{0}\n'.format(self.description))
        fp.write('  color={0}\n'.format(self._color))
        if self._color != OBJECT_COLOR:
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
    """Pen style container"""
    def __init__(self, description="", scale_factor=1.0, apply_factor=False):
        self.description = description
        self.scale_factor = scale_factor
        self.apply_factor = apply_factor

        # set custom_line... to 1 for showing lineweights in inch in the Autocad
        # ctb editor window, but lineweights are always defined in mm
        self.custom_lineweight_display_units = 0
        self.styles = [None] * (STYLE_COUNT+1)
        self.lineweights = array('f', DEFAULT_LINE_WEIGHTS)
        self.set_default_styles()

    def set_default_styles(self):
        for index in xrange(STYLE_COUNT):
            pen = Pen(index)
            self._set_pen(pen)

    @staticmethod
    def check_color_index(color_index):
        if 0 < color_index < 256:
            return color_index
        raise IndexError('color index has to be in th range [1 .. 255].')

    def iter_styles(self):
        return (style for style in self.styles[1:])

    def _set_pen(self, pen):
        self.styles[pen.get_dxf_color_index()] = pen

    def set_style(self, color_index, init_dict={}):
        """Set <color_index> to new attributes defined in init_dict.

        color_index -- is the dxf color index
        """
        color_index=self.check_color_index(color_index)
        # ctb table index is dxf color index - 1
        # ctb table starts with index 0, where dxf color index 0 means BYBLOCK
        pen = Pen(color_index-1, init_dict)
        self._set_pen(pen)
        return pen

    def get_style(self, color_index):
        """Get style for <color_index>.

        color_index -- is the dxf color index
        """
        return self.styles[color_index]

    # interface for dxfwrite.std.color_index()
    def get_color(self, dxf_color_index):
        """Get rgb-color-tuple for <dxf_color_index> or None if not specified.
        """
        pen = self.get_style(dxf_color_index)
        return pen.get_color()

    def set_lineweight(self, index, weight):
        """Index is the lineweight table index, not the dxf color index.

        index -- lineweight table index = Pen.lineweight
        weight -- in millimeters
        """
        try:
            self.lineweights[index] = weight
            return index
        except IndexError:
            self.lineweights.append(weight)
            return len(self.lineweights)-1

    def get_lineweight(self, index):
        """Returns lineweight in millimeters.

        returns 0.0 for: use object lineweight

        index -- lineweight table index = Pen.lineweight
        """
        return self.lineweights[index]

    def get_pen_lineweight(self, pen):
        """Returns the lineweight of pen in millimeters.

        returns 0.0 for: use object lineweight

        pen -- Pen object
        """
        return self.lineweights[pen.lineweight]

    def write(self, fp):
        """Create and compress the ctb-file to <fp>."""
        memfile=StringIO()
        self.write_content(memfile)
        memfile.write(chr(0)) # end of file
        body = memfile.getvalue()
        memfile.close()
        self._compress(fp, body)

    def write_content(self, fp):
        """Write the ctb-file to <fp>."""
        self._write_header(fp)
        self._write_aci_table(fp)
        self._write_ctb_plot_styles(fp)
        self._write_lineweights(fp)

    def _write_header(self, fp):
        """Write header values of ctb-file to <fp>."""
        fp.write('description="{0}\n'.format(self.description))
        fp.write('aci_table_available=TRUE\n')
        fp.write('scale_factor={0:.1f}\n'.format(self.scale_factor))
        fp.write('apply_factor={0}\n'.format(unicode(self.apply_factor).upper()))
        fp.write('custom_lineweight_display_units={0}\n'.format(
            self.custom_lineweight_display_units))

    def _write_aci_table(self, fp):
        """Write autocad color index table to ctb-file <fp>."""
        fp.write('aci_table{\n')
        for style in self.iter_styles():
            index = style.index
            fp.write(' {0}="{1}\n'.format(index, color_name(index)))
        fp.write('}\n')

    def _write_ctb_plot_styles(self, fp):
        """Write pen styles to ctb-file <fp>."""
        fp.write('plot_style{\n')
        for style in self.iter_styles():
            style.write(fp)
        fp.write('}\n')

    def _write_lineweights(self, fp):
        """Write custom lineweights table to ctb-file <fp>."""
        fp.write('custom_lineweight_table{\n')
        for index, weight in enumerate(self.lineweights):
            fp.write(' {0}={1}\n'.format(index, weight))
        fp.write('}\n')

    def parse(self, text):
        """Parse and get values of plot styles from <text>."""
        def set_lineweights(lineweights):
            if lineweights is None:
                return
            self.lineweights = array('f', [0.0] * len(lineweights))
            for key, value in lineweights.iteritems():
                self.lineweights[int(key)] = float(value)

        parser = CtbParser(text)
        self.description = parser.get('description', "")
        self.scale_factor = float(parser.get('scale_factor', 1.0))
        self.apply_factor = (parser.get('apply_factor', 1.0).upper() == 'TRUE')
        self.custom_lineweight_display_units = int(
            parser.get('custom_lineweight_display_units', 1.0))
        set_lineweights(parser.get('custom_lineweight_table', None))
        styles = parser.get('plot_style', {})
        for index, style in styles.iteritems():
            pen = Pen(index, style)
            self._set_pen(pen)

    def _compress(self, fp, body):
        """Compress ctb-file-body and write it to <fp>."""
        header = 'PIAFILEVERSION_2.0,CTBVER1,compress\r\npmzlibcodec'
        fp.write(header)
        full_len = len(body)
        comp_body = zlib.compress(body)
        comp_len = len(comp_body)
        adler = zlib.adler32(comp_body)
        fp.write(pack('LLL', adler, full_len, comp_len))
        fp.write(comp_body)

def read(fp):
    """Read a ctb-file from the file-like object <fp>.
    Returns a PenStyle object.
    """
    content = _decompress(fp)
    styles = PenStyles()
    styles.parse(content)
    return styles

def _decompress(fp):
    """Read and decompress the file content of the file-like object <fp>."""
    content = fp.read()
    text = zlib.decompress(content[60:])
    return text[:-1] # truncate trailing \nul

class CtbParser(object):
    """A very simple ctb-file parser. Ctb-files are created by programms, so the
    file structure should be correct in the most cases.
    """
    def __init__(self, text):
        """Construtor

        text -- ctb content
        """
        self.data = {}
        for element, value in self.iter_elements(text):
            self.data[element] = value

    def iter_elements(self, text):
        """iterate over all first level (start at col 0) elements"""
        def get_name(num):
            """Get element name of line <num>.
            """
            line = lines[num]
            if line.endswith('{'): # start of a list like 'plot_style{'
                name = line[:-1]
            else: # simple name=value line
                name = line.split('=', 1)[0]
            return name.strip()

        def get_list(num):
            """Get list of elements enclosed by { }.

            lineweigths, plot_styles, aci_table
            """
            data = dict()
            while not lines[num].endswith('}'): # while not end of list
                name = get_name(num)
                num, value = get_value(num) # get value or sub-list
                data[name] = value
            return num+1, data

        def get_value(num):
            """Get value of line <num> or the list that starts in line <num>."""
            line=lines[num]
            if line.endswith('{'): # start of a list
                num, value = get_list(num+1)
            else: # it's a simple name=value line
                value = line.split('=', 1)[1]
                value = value.lstrip('"') # strings look like this: name="value
                num += 1
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
    """Convert color integer value from ctb-file to rgb-tuple plus a magic number.
    """
    magic = (color & 0xff000000) >> 24 # is 0xc3 or 0xc2 don't know what this value means
    red = (color & 0xff0000) >> 16
    green = (color & 0xff00) >> 8
    blue = color & 0xff
    return (red, green, blue, magic)

def mode_color2int(red, green, blue, magic=0xc2):
    """Convert rgb-tuple to an int value."""
    return -color2int(red, green, blue, magic)

def color2int(red, green, blue, magic):
    """Convert rgb-tuple to an int value."""
    return -((magic << 24) + (red << 16) + (green << 8) + blue) & 0xffffffff

if __name__ == "__main__":
    #ctb_in = r'D:\User\Python\ctb\eis.ctb'
    #with open(ctb_in, 'rb') as filepointer:
    #    ctb = read(filepointer)
    ctb = PenStyles('test acadctb.py')
    pen1=ctb.set_style(1, {'description': 'object_color'})
    pen1.set_object_color()
    pen2=ctb.get_style(2)
    pen2.description="grey-grey-grey"
    pen2.set_color(234,234,234)
    pen2.grayscale=True
    pen2.dithering=False

    with open(r'D:\User\Python\ctb\test.ctb', 'wb') as filepointer:
        ctb.write(filepointer)
