.. _ARC:

ARC
===

Type: Basic DXF R12 entity.

Draws circular arcs — arcs cut from circles, not from ellipses,
parabolas, or some other complicated curve, the arc goes from start angle
to end angle.

.. method:: DXFEngine.arc(radius=1.0, center=(0., 0.), startangle=0., endangle=360., **kwargs)

    :param float radius: arc radius
    :param center: center point (xy- or xyz-tuple), z-axis is 0 by default
    :param float startangle: start angle in degree
    :param float endangle: end angle in degree

Common Keyword Arguments for all Basic DXF R12 Entities
-------------------------------------------------------

=================== =========================================================
keyword             description
=================== =========================================================
layer               Layer name as string
linetype            Linetype name as string, if not defined = BYLAYER
color               as integer in range [1..255], 0 = BYBLOCK, 256 = BYLAYER
thickness           Thickness as float
paper_space         0 = entity is in model_space, 1 = entity is in
                    paper_space
extrusion_direction 3D Point as tuple(x, y, z) if extrusion direction is not
                    parallel to the World Z axis
=================== =========================================================

Attribs of DXF entities can be changed by the index operator::

  from dxfwrite import DXFEngine as dxf

  drawing = dxf.drawing('drawing.dxf')
  arc = dxf.arc(2.0, (1.0, 1.0), 30, 90)
  arc['layer'] = 'points'
  arc['color'] = 7
  arc['center'] = (2, 3, 7) # int or float
  arc['radius'] = 3.5
  drawing.add(arc)
  drawing.save()

