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

.. method:: Table.set_col_width(column, value)

    Set width of 'column' to 'value'.

    :param int column: zero based column index
    :param float value: new column width in drawing units

.. method:: Table.set_row_height(row, value)

    Set height of 'row' to 'value'.

    :param int row: zero based row index
    :param float value: new row height in drawing units

.. method:: Table.text_cell(row, col, text, span=(1, 1), style='default')

    Create a new text cell at position (row, col), with 'text' as
    content, text can be a multi-line text, use ``'\\n'`` as line
    separator.

    The cell spans over **span** cells and has the cell style with the
    name **style**.

.. method:: Table.block_cell(row, col, blockdef, span=(1, 1), attribs={}, style='default')

    Create a new block cell at position (row, col).

    Content is a block reference inserted by a :ref:`INSERT` entity,
    attributes will be added if the block definition contains :ref:`ATTDEF`.
    Assignments are defined by attribs-key to attdef-tag association.

    Example: attribs = {'num': 1} if an :ref:`ATTDEF` with tag=='num' in
    the block definition exists, an attrib with text=str(1) will be
    created and added to the insert entity.

    The cell spans over 'span' cells and has the cell style with the
    name 'style'.

.. method:: Table.set_cell(row, col, cell)

    Insert a cell at position (row, col).

.. method:: Table.get_cell(row, col)

    Get cell at position (row, col).

.. method:: Table.frame(row, col, width=1, height=1, style='default')

    Create a Frame object which frames the cell area starting at (row, col),
    covering 'width' columns and 'height' rows.

.. method:: Table.new_cell_style(name, **kwargs)

    Create a new Style object 'name'.

    The 'kwargs' are the key, value pairs of of the dict :ref:`CellStyle`.

.. method:: Table.new_border_style(color=const.BYLAYER, status=True, priority=100, linetype=None):

    Create a new border style.

    :param bool status: True for visible, else False
    :param int color: dxf color index
    :param string linetype: linetype name, BYLAYER if None
    :param int priority: drawing priority - higher values covers lower values

    see also :ref:`BorderStyle`.


.. method:: Table.get_cell_style(name)

    Get cell style by name.

.. method:: Table.iter_visible_cells

    Iterate over all visible cells.

    :returns: a generator which yields all visible cells as tuples: (row , col, cell)

.. _CellStyle:

Cellstyle
----------

Just a python dict::

    {
        # textstyle is ignored by block cells
        'textstyle': 'STANDARD',
        # text height in drawing units, ignored by block cells
        'textheight': DEFAULT_CELL_TEXT_HEIGHT,
        # line spacing in percent = <textheight>*<linespacing>, ignored by block cells
        'linespacing': DEFAULT_CELL_LINESPACING,
        # text stretch or block reference x-axis scaling factor
        'xscale': DEFAULT_CELL_XSCALE,
        # block reference y-axis scaling factor, ignored by text cells
        'yscale': DEFAULT_CELL_YSCALE,
        # dxf color index, ignored by block cells
        'textcolor': DEFAULT_CELL_TEXTCOLOR,
        # text or block rotation in degrees
        'rotation' : 0.,
        # Letters are stacked top-to-bottom, but not rotated
        'stacked': False,
        # horizontal alignment (const.LEFT, const.CENTER, const.RIGHT)
        'halign': DEFAULT_CELL_HALIGN,
        # vertical alignment (const.TOP, const.MIDDLE, const.BOTTOM)
        'valign': DEFAULT_CELL_VALIGN,
        # left and right margin in drawing units
        'hmargin': DEFAULT_CELL_HMARGIN,
        # top and bottom margin
        'vmargin': DEFAULT_CELL_VMARGIN,
        # background color, dxf color index, ignored by block cells
        'bgcolor': DEFAULT_CELL_BG_COLOR,
        # left border style
        'left': Style.get_default_border_style(),
        # top border style
        'top': Style.get_default_border_style(),
        # right border style
        'right': Style.get_default_border_style(),
        # bottom border style
        'bottom': Style.get_default_border_style(),
    }

.. _BorderStyle:

Borderstyle
-----------

Just a python dict::

    {
        # border status, True for visible, False for hidden
        'status': DEFAULT_BORDER_STATUS,
        # dxf color index
        'color': DEFAULT_BORDER_COLOR,
        # linetype name, BYLAYER if None
        'linetype': DEFAULT_BORDER_LINETYPE,
        # drawing priority, higher values cover lower values
        'priority': DEFAULT_BORDER_PRIORITY,
    }


Example
-------

.. literalinclude:: ../../examples/table.py
   :lines: 22-

.. image:: table.png

