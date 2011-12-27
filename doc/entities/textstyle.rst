.. _Textstyle:

TEXTSTYLE
=========

The DXF format assigns text properties to individual lines of text based on text styles.
These text styles are similar to the paragraph styles in a word processor; they
contain font and other settings that determine the look and feel of text.

A DXF text style includes:
--------------------------

* The font
* A text height, which you can set or leave at 0 for later flexibility
* Special effects (where available), such as italic
* Really special effects, such as vertical and upside down

To use the textstyles just assign the stylename as string.

Predefined text styles for all drawings created with dxfwrite:

================== ==============================
Stylename          True Type Font
================== ==============================
STANDARD           arial.ttf
ARIAL              arial.ttf
ARIAL_BOLD         arialbd.ttf
ARIAL_ITALIC       ariali.ttf
ARIAL_BOLD_ITALIC  arialbi.ttf
ARIAL_BLACK        ariblk.ttf
ISOCPEUR           isocpeur.ttf
ISOCPEUR_ITALIC    isocpeui.ttf
TIMES              times.ttf
TIMES_BOLD         timesbd.ttf
TIMES_ITALIC       timesi.ttf
TIMES_BOLD_ITALIC  timesbi.ttf
================== ==============================

Create a Textstyle::

    drawing.add_style(stylename)

is a shortcut for::

    style = DXFEngine.style(name)
    drawing.styles.add(style)

.. method:: DXFEngine.style(name, **kwargs)

    :param string name: textstyle name
    :param int flags: standard flag values, bit-coded, default=0
    :param int generation_flags: text generation flags, default = 0
    :param float height: fixed text height, 0 if not fixed = default
    :param last_height: last height used, default=1.
    :param float width: width factor, default=1.
    :param float oblique: oblique angle in degree, default=0.
    :param string font: primary font filename, default="ARIAL"
    :param string bigfont: big-font file name, default=""

Generation Flags
----------------

=====================  ===================================
        Flag                        Description
=====================  ===================================
STYLE_TEXT_BACKWARD    Text is backward (mirrored in X)
STYLE_TEXT_UPSIDEDOWN  Text is upside down (mirrored in Y)
=====================  ===================================

A text style **height of 0.0** makes the style variable height, which means
that you can specify the height separately for each text object. Assigning
a fixed (that is, nonzero) height to a text style forces all text using the
style to be the same height. Variable height styles are more flexible, but
fixed height styles usually make it easier to draw text of consistent
height.
