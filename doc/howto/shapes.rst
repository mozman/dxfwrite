Shapes Management
=================

How to set/get DXF attributes?
------------------------------

This is common to all **basic** DXF entities (not valid for composite entities)::

    # as keyword arguments
    line = DXFEngine.line((0,0), (1,1), layer='TESTLAYER', linetype='DASHED', color=1)

    # or:
    line['layer'] = 'TESTLAYER'
    line['linetype'] = 'DASHED'
    line['color'] = 1
