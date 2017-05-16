from dxfwrite import DXFEngine as dxf

dwg = dxf.drawing('polyline.dxf')

points = [(0, 3), (2, 0), (5, 0), (7, 3), (5, 6), (2, 6)]
polyline = dxf.polyline(points)
polyline.close()
dwg.add(polyline)

dwg.save()
