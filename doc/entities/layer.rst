.. _Layer:

LAYER
=====

Every object has a layer as one of its properties. You may be familiar with
layers - independent drawing spaces that stack on top of each other to
create an overall image - from using drawing programs. Most
CAD programs, uses layers as the primary organizing principle for all the
objects that you draw. You use layers to organize objects into logical groups
of things that belong together; for example, walls, furniture, and text notes
usually belong on three separate layers, for a couple of reasons:

* Layers give you a way to turn groups of objects on and off - both on the screen and on the plot.
* Layers provide the most efficient way of controlling object color and linetype

First you have to create layers, assigning them names and properties such as
color and linetype. Then you can assign those layers to other darwing entities.
To assign a layer just use its name as string.

Create a layer::

    drawing.add_layer(name)

is a shortcut for::

    layer = DXFEngine.layer(name)
    drawing.layers.add(layer)


.. method:: DXFEngine.layer(name, **kwargs)

    :param string name: layer name
    :param int flags: standard flag values, bit-coded, default=0
    :param int color: color number, negative if layer is off, default=1
    :param string linetype: linetype name, default="CONTINUOUS"

Flags
-----

=================================  ===================================
              Flag                             Description
=================================  ===================================
LAYER_FROZEN                       If set, layer is frozen
LAYER_FROZEN_BY_DEFAULT            If set, layer is frozen by default
                                   in new Viewports
LAYER_LOCKED                       If set, layer is locked
=================================  ===================================

Get :class:`Layer` ``'name'`` from Drawing::

    layer = drawing.layers['name']
    layer.off()

.. class:: Layer

    Defines the layer properties. Get/set properties by the subscript operator `[ ]`.

    - ``layer['name']``
    - ``layer['flags']`` (for status change see also special methods below)
    - ``layer['color']``
    - ``layer['linetype']``

.. method:: Layer.on()

.. method:: Layer.off()

.. method:: Layer.freeze()

.. method:: Layer.thaw()

.. method:: Layer.lock()

.. method:: Layer.unlock()



Example::

    from dxfwrite import DXFEngine as dxf

    drawing = dxf.drawing('drawing.dxf')
    drawing.add_layer('LINES', color=3, linetype='DASHED')
    line = dxf.line((1.2, 3.7), (5.5, 9.7), layer='LINES')
    drawing.add(line)
    drawing.save()

