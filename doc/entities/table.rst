.. _Table:

Table
=====

Type: Composite Entity

Table object like a HTML-Table, buildup with basic DXF R12 entities.

Cells can contain Multiline-Text or DXF-BLOCKs, or you can create your own
cell-type by extending the CustomCell object.

Cells can span over columns and rows.

Text cells can contain text with an arbitrary rotation angle, or letters can be
stacked top-to-bottom.

BlockCells contains block references (INSERT-entity) created from a block
definition (BLOCK), if the block definition contains attribute definitions
(ATTDEF-entity), attribs created by Attdef.new_attrib() will be added to the
block reference (ATTRIB-entity).

.. method:: DXFEngine.table(insert, nrows, ncols, default_grid=True)

    :param insert: insert point as 2D or 3D point
    :param int nrows: row count
    :param int ncols: column count
    :param bool default_grid: if **True** always a solid line grid will
        be drawn, if **False**, only explicit defined borders will be
        drawn, default grid has a priority of 50.


Methods
-------

.. method:: Table.set_col_width

.. method:: Table.set_row_height

.. method:: Table.text_cell

.. method:: Table.block_cell

.. method:: Table.set_cell

.. method:: Table.get_cell

.. method:: Table.frame

.. method:: Table.new_cell_style

.. method:: Table.new_border_style

.. method:: Table.get_cell_style

.. method:: Table.iter_visible_cells

Example
-------

.. literalinclude:: ../../examples/table.py
   :lines: 22-

.. image:: table.png

