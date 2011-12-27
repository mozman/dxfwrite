.. _Linetype:

Linetypes
=========

A Linetype defines a line pattern, which can be used by DXF entities. A Linepattern can contain
solid line elements, points and gaps (see :ref:`Linepattern`).

Create a linetype::

    drawing.add_linetype(name, pattern=linepattern)

is a shortcut for::

    linetype = DXFEngine.linetype(name, pattern=linepattern)
    drawing.linetypes.add(linetype)

.. method:: DXFEngine.linetype(name, **kwargs)

    :param string name: linetype name
    :param int flags: standard flag values, bit-coded, default=0
    :param string description: descriptive text for linetype, default=""
    :param pattern: line pattern definition, see method `DXFEngine.linepattern`

The following Linetypes are predefined by dxfwrite::

    CONTINUOUS: Solid
    CENTER: Center ____ _ ____ _ ____ _ ____ _ ____ _ ____
    CENTERX2: Center (2x) ________  __  ________  __  ________
    CENTER2: Center (.5x) ____ _ ____ _ ____ _ ____ _ ____
    DASHED: Dashed __ __ __ __ __ __ __ __ __ __ __ __ __ _
    DASHEDX2: Dashed (2x) ____  ____  ____  ____  ____  ____
    DASHED2:Dashed (.5x) _ _ _ _ _ _ _ _ _ _ _ _ _ _
    PHANTOM: Phantom ______  __  __  ______  __  __  ______
    PHANTOMX2: Phantom (2x)____________    ____    ____    ____________
    PHANTOM2: Phantom (.5x) ___ _ _ ___ _ _ ___ _ _ ___ _ _ ___
    DASHDOT: Dash dot __ . __ . __ . __ . __ . __ . __ . __
    DASHDOTX2: Dash dot (2x) ____  .  ____  .  ____  .  ____
    DASHDOT2: Dash dot (.5x) _ . _ . _ . _ . _ . _ . _ . _
    DOT: Dot .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    DOTX2: Dot (2x) .    .    .    .    .    .    .    .
    DOT2: Dot (.5) . . . . . . . . . . . . . . . . . . .
    DIVIDE: Divide __ . . __ . . __ . . __ . . __ . . __
    DIVIDEX2: Divide (2x) ____  . .  ____  . .  ____  . .  ____
    DIVIDE2: Divide (.5) _ . _ . _ . _ . _ . _ . _ . _


.. _Linepattern:

Linepattern
===========

Create a linepattern::

    linepattern = DXFEngine.linepattern(pattern)


.. method:: DXFEngine.linepattern(pattern)

    :param pattern: is a list of float values, elements > 0 are solid line segments,
        elements < 0 are gaps and elements = 0 are points. pattern[0] = total pattern
        length in drawing units

example linepattern([2.0, 1.25, -0.25, 0, -0.25])

