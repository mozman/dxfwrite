.. _HEADER:

HEADER Section
==============

The HEADER section of the DXF file contains settings of variables
associated with the drawing. The following list shows the header
variables and their meanings.

set/get header variables::

    #set value
    drawing.header['$ANGBASE'] = 30
    drawing.header['$EXTMIN'] = (0, 0, 0)
    drawing.header['$EXTMAX'] = (100, 100, 0)

    #get value
    version = drawing.header['$ACADVER'].value

    # for 2D/3D points use:
    minx, miny, minz = drawing.header['$EXTMIN'].tuple
    maxx, maxy, maxz = drawing.header['$EXTMAX'].tuple

+----------------+--------+-------------------------------------+
| Variable       | Type   | Description                         |
+================+========+=====================================+
| $ACADVER       | string | The AutoCAD drawing database        |
|                |        | version number; AC1006 = R10,       |
|                |        | AC1009 = R11 and R12                |
+----------------+--------+-------------------------------------+
| $ANGBASE       | float  | Angle 0 direction                   |
+----------------+--------+-------------------------------------+
| $ANGDIR        | int    | 1 = clockwise angles, 0 =           |
|                |        | counterclockwise                    |
+----------------+--------+-------------------------------------+
| $ATTDIA        | int    | Attribute entry dialogs, 1 = on,    |
|                |        | 0 = off                             |
+----------------+--------+-------------------------------------+
| $ATTMODE       | int    | Attribute visibility: 0 = none,     |
|                |        | 1 = normal, 2 = all                 |
+----------------+--------+-------------------------------------+
| $ATTREQ        | int    | Attribute prompting during INSERT,  |
|                |        | 1 = on, 0 = off                     |
+----------------+--------+-------------------------------------+
| $AUNITS        | int    | Units format for angles             |
+----------------+--------+-------------------------------------+
| $AUPREC        | int    | Units precision for angles          |
+----------------+--------+-------------------------------------+
| $AXISMODE      | int    | Axis on if nonzero (not functional  |
|                |        | in Release 12)                      |
+----------------+--------+-------------------------------------+
| $AXISUNIT      | 2DPoint| Axis X and Y tick spacing           |
|                |        | (not functional in Release 12)      |
+----------------+--------+-------------------------------------+
| $BLIPMODE      | int    | Blip mode on if nonzero             |
+----------------+--------+-------------------------------------+
| $CECOLOR       | int    | Entity color number; 0 = BYBLOCK,   |
|                |        | 256 = BYLAYER                       |
+----------------+--------+-------------------------------------+
| $CELTYPE       | string | Entity linetype name, or BYBLOCK    |
|                |        | or BYLAYER                          |
+----------------+--------+-------------------------------------+
| $CHAMFERA      | float  | First chamfer distance              |
+----------------+--------+-------------------------------------+
| $CHAMFERB      | float  | Second chamfer distance             |
+----------------+--------+-------------------------------------+
| $CLAYER        | string | Current layer name                  |
+----------------+--------+-------------------------------------+
| $COORDS        | int    | 0 = static coordinate display,      |
|                |        | 1 = continuous update, 2 = "d<a"    |
|                |        | format                              |
+----------------+--------+-------------------------------------+
| $DIMALT        | int    | Alternate unit dimensioning         |
|                |        | performed if nonzero                |
+----------------+--------+-------------------------------------+
| $DIMALTD       | int    | Alternate unit decimal places       |
+----------------+--------+-------------------------------------+
| $DIMALTF       | float  | Alternate unit scale factor         |
+----------------+--------+-------------------------------------+
| $DIMAPOST      | string | Alternate dimensioning suffix       |
+----------------+--------+-------------------------------------+
| $DIMASO        | int    | 1 = create associative dimensioning,|
|                |        | 0 = draw individual entities        |
+----------------+--------+-------------------------------------+
| $DIMASZ        | float  | Dimensioning arrow size             |
+----------------+--------+-------------------------------------+
| $DIMBLK        | string | Arrow block name                    |
+----------------+--------+-------------------------------------+
| $DIMBLK1       | string | First arrow block name              |
+----------------+--------+-------------------------------------+
| $DIMBLK2       | string | Second arrow block name             |
+----------------+--------+-------------------------------------+
| $DIMCEN        | float  | Size of center mark/lines           |
+----------------+--------+-------------------------------------+
| $DIMCLRD       | int    | Dimension line color, range is      |
|                |        | 0 = BYBLOCK, 256 = BYLAYER          |
+----------------+--------+-------------------------------------+
| $DIMCLRE       | int    | Dimension extension line color,     |
|                |        | range is 0 = BYBLOCK, 256 = BYLAYER |
+----------------+--------+-------------------------------------+
| $DIMCLRT       | int    | Dimension text color, range is      |
|                |        | 0 = BYBLOCK, 256 = BYLAYER          |
+----------------+--------+-------------------------------------+
| $DIMDLE        | float  | Dimension line extension            |
+----------------+--------+-------------------------------------+
| $DIMDLI        | float  | Dimension line increment            |
+----------------+--------+-------------------------------------+
| $DIMEXE        | float  | Extension line extension            |
+----------------+--------+-------------------------------------+
| $DIMEXO        | float  | Extension line offset               |
+----------------+--------+-------------------------------------+
| $DIMGAP        | float  | Dimension line gap                  |
+----------------+--------+-------------------------------------+
| $DIMLFAC       | float  | Linear measurements scale factor    |
+----------------+--------+-------------------------------------+
| $DIMLIM        | int    | Dimension limits generated if       |
|                |        | nonzero                             |
+----------------+--------+-------------------------------------+
| $DIMPOST       | string | General dimensioning suffix         |
+----------------+--------+-------------------------------------+
| $DIMRND        | float  | Rounding value for dimension        |
|                |        | distances                           |
+----------------+--------+-------------------------------------+
| $DIMSAH        | int    | Use separate arrow blocks if nonzero|
+----------------+--------+-------------------------------------+
| $DIMSCALE      | float  | Overall dimensioning scale factor   |
+----------------+--------+-------------------------------------+
| $DIMSE1        | int    | First extension line suppressed     |
|                |        | if nonzero                          |
+----------------+--------+-------------------------------------+
| $DIMSE2        | int    | Second extension line suppressed    |
|                |        | if nonzero                          |
+----------------+--------+-------------------------------------+
| $DIMSHO        | int    | 1 = Recompute dimensions while      |
|                |        | dragging, 0 = drag original image   |
+----------------+--------+-------------------------------------+
| $DIMSOXD       | int    | Suppress outside-extensions         |
|                |        | dimension lines if nonzero          |
+----------------+--------+-------------------------------------+
| $DIMSTYLE      | string | Dimension style name                |
+----------------+--------+-------------------------------------+
| $DIMTAD        | int    | Text above dimension line if nonzero|
+----------------+--------+-------------------------------------+
| $DIMTFAC       | float  | Dimension tolerance display scale   |
|                |        | factor                              |
+----------------+--------+-------------------------------------+
| $DIMTIH        | int    | Text inside horizontal if nonzero   |
+----------------+--------+-------------------------------------+
| $DIMTIX        | int    | Force text inside extensions if     |
|                |        | nonzero                             |
+----------------+--------+-------------------------------------+
| $DIMTM         | float  | Minus tolerance                     |
+----------------+--------+-------------------------------------+
| $DIMTOFL       | int    | If text outside extensions, force   |
|                |        | line extensions between extensions  |
|                |        | if nonzero                          |
+----------------+--------+-------------------------------------+
| $DIMTOH        | int    | Text outside horizontal if nonzero  |
+----------------+--------+-------------------------------------+
| $DIMTOL        | int    | Dimension tolerances generated if   |
|                |        | nonzero                             |
+----------------+--------+-------------------------------------+
| $DIMTP         | float  | Plus tolerance                      |
+----------------+--------+-------------------------------------+
| $DIMTSZ        | float  | Dimensioning tick size: 0 = no ticks|
+----------------+--------+-------------------------------------+
| $DIMTVP        | float  | Text vertical position              |
+----------------+--------+-------------------------------------+
| $DIMTXT        | float  | Dimensioning text height            |
+----------------+--------+-------------------------------------+
| $DIMZIN        | int    | Zero suppression for "feet & inch"  |
|                |        | dimensions                          |
+----------------+--------+-------------------------------------+
| $DWGCODEPAGE   | int    | Drawing code page. Set to the       |
|                |        | system code page when a new drawing |
|                |        | is created, but not otherwise       |
|                |        | maintained by AutoCAD               |
+----------------+--------+-------------------------------------+
| $DRAGMODE      | int    | 0 = off, 1 = on, 2 = auto           |
+----------------+--------+-------------------------------------+
| $ELEVATION     | float  | Current elevation set by ELEV       |
|                |        | command                             |
+----------------+--------+-------------------------------------+
| $EXTMAX        | 3DPoint| X, Y, and Z drawing extents         |
|                |        | upper-right corner (in WCS)         |
+----------------+--------+-------------------------------------+
| $EXTMIN        | 3DPoint| X, Y, and Z drawing extents         |
|                |        | lower-left corner (in WCS)          |
+----------------+--------+-------------------------------------+
| $FILLETRAD     | float  | Fillet radius                       |
+----------------+--------+-------------------------------------+
| $FILLMODE      | int    | Fill mode on if nonzero             |
+----------------+--------+-------------------------------------+
| $HANDLING      | int    | Handles enabled if nonzero          |
+----------------+--------+-------------------------------------+
| $HANDSEED      | string | Next available handle               |
+----------------+--------+-------------------------------------+
| $INSBASE       | 3DPoint| Insertion base set by BASE command  |
|                |        | (in WCS)                            |
+----------------+--------+-------------------------------------+
| $LIMCHECK      | int    | Nonzero if limits checking is on    |
+----------------+--------+-------------------------------------+
| $LIMMAX        | 2DPoint| XY drawing limits upper-right       |
|                |        | corner (in WCS)                     |
+----------------+--------+-------------------------------------+
| $LIMMIN        | 2DPoint| XY drawing limits lower-left        |
|                |        | corner (in WCS)                     |
+----------------+--------+-------------------------------------+
| $LTSCALE       | float  | Global linetype scale               |
+----------------+--------+-------------------------------------+
| $LUNITS        | int    | Units format for coordinates and    |
|                |        | distances                           |
+----------------+--------+-------------------------------------+
| $LUPREC        | int    | Units precision for coordinates     |
|                |        | and distances                       |
+----------------+--------+-------------------------------------+
| $MAXACTVP      | int    | Sets maximum number of viewports to |
|                |        | be regenerated                      |
+----------------+--------+-------------------------------------+
| $MENU          | string | Name of menu file                   |
+----------------+--------+-------------------------------------+
| $MIRRTEXT      | int    | Mirror text if nonzero              |
+----------------+--------+-------------------------------------+
| $ORTHOMODE     | int    | Ortho mode on if nonzero            |
+----------------+--------+-------------------------------------+
| $OSMODE        | int    | Running object snap modes           |
+----------------+--------+-------------------------------------+
| $PDMODE        | int    | Point display mode                  |
+----------------+--------+-------------------------------------+
| $PDSIZE        | float  | Point display size                  |
+----------------+--------+-------------------------------------+
| $PELEVATION    | float  | Current paper space elevation       |
+----------------+--------+-------------------------------------+
| $PEXTMAX       | 3DPoint| Maximum X, Y, and Z extents for     |
|                |        | paper space                         |
+----------------+--------+-------------------------------------+
| $PEXTMIN       | 3DPoint| Minimum X, Y, and Z extents for     |
|                |        | paper space                         |
+----------------+--------+-------------------------------------+
| $PLIMCHECK     | int    | Limits checking in paper space      |
|                |        | when nonzero                        |
+----------------+--------+-------------------------------------+
| $PLIMMAX       | 2DPoint| Maximum X and Y limits in paper     |
|                |        | space                               |
+----------------+--------+-------------------------------------+
| $PLIMMIN       | 2DPoint| Minimum X and Y limits in paper     |
|                |        | space                               |
+----------------+--------+-------------------------------------+
| $PLINEGEN      | int    | Governs the generation of linetype  |
|                |        | patterns around the vertices        |
|                |        | of a 2D Polyline                    |
|                |        | 1 = linetype is generated in        |
|                |        | a continuous pattern around         |
|                |        | vertices of the Polyline            |
|                |        | 0 = each segment of the Polyline    |
|                |        | starts and ends with a dash         |
+----------------+--------+-------------------------------------+
| $PLINEWID      | float  | Default Polyline width              |
+----------------+--------+-------------------------------------+
| $PSLTSCALE     | int    | Controls paper space linetype       |
|                |        | scaling                             |
|                |        | 1 = no special linetype scaling     |
|                |        | 0 = viewport scaling governs        |
|                |        | linetype scaling                    |
+----------------+--------+-------------------------------------+
| $PUCSNAME      | string | Current paper space UCS name        |
+----------------+--------+-------------------------------------+
| $PUCSORG       | 3DPoint| Current paper space UCS origin      |
|                |        |                                     |
+----------------+--------+-------------------------------------+
| $PUCSXDIR      | 3DPoint| Current paper space UCS X axis      |
|                |        |                                     |
+----------------+--------+-------------------------------------+
| $PUCSYDIR      | 3DPoint| Current paper space UCS Y axis      |
|                |        |                                     |
+----------------+--------+-------------------------------------+
| $QTEXTMODE     | int    | Quick text mode on if nonzero       |
+----------------+--------+-------------------------------------+
| $REGENMODE     | int    | REGENAUTO mode on if nonzero        |
+----------------+--------+-------------------------------------+
| $SHADEDGE      | int    | 0 = faces shaded, edges not         |
|                |        | highlighted                         |
|                |        | 1 = faces shaded, edges highlighted |
|                |        | in black                            |
|                |        | 2 = faces not filled, edges in      |
|                |        | entity color                        |
|                |        | 3 = faces in entity color,          |
|                |        | edges in black                      |
+----------------+--------+-------------------------------------+
| $SHADEDIF      | int    | Percent ambient/diffuse light,      |
|                |        | range 1-100, default 70             |
+----------------+--------+-------------------------------------+
| $SKETCHINC     | float  | Sketch record increment             |
+----------------+--------+ 0 = sketch lines, 1 = sketch        |
| $SKPOLY        | int    | polylines                           |
+----------------+--------+-------------------------------------+
| $SPLFRAME      | int    | Spline control polygon display,     |
|                |        | 1 = on, 0 = off                     |
+----------------+--------+-------------------------------------+
| $SPLINESEGS    | int    | Number of line segments per spline  |
|                |        | patch                               |
+----------------+--------+-------------------------------------+
| $SPLINETYPE    | int    | Spline curve type for PEDIT Spline  |
|                |        | (See your AutoCAD Reference Manual) |
+----------------+--------+-------------------------------------+
| $SURFTAB1      | int    | Number of mesh tabulations in first |
|                |        | direction                           |
+----------------+--------+-------------------------------------+
| $SURFTAB2      | int    | Number of mesh tabulations in       |
|                |        | second direction                    |
+----------------+--------+-------------------------------------+
| $SURFTYPE      | int    | Surface type for PEDIT Smooth       |
|                |        | (See your AutoCAD Reference Manual) |
+----------------+--------+-------------------------------------+
| $SURFU         | int    | Surface density (for PEDIT Smooth)  |
|                |        | in M direction                      |
+----------------+--------+-------------------------------------+
| $SURFV         | int    | Surface density (for PEDIT Smooth)  |
|                |        | in N direction                      |
+----------------+--------+-------------------------------------+
| $TDCREATE      | float  | Date/time of drawing creation       |
+----------------+--------+-------------------------------------+
| $TDINDWG       | float  | Cumulative editing time for         |
|                |        | this drawing                        |
+----------------+--------+-------------------------------------+
| $TDUPDATE      | float  | Date/time of last drawing update    |
+----------------+--------+-------------------------------------+
| $TDUSRTIMER    | float  | User elapsed timer                  |
+----------------+--------+-------------------------------------+
| $TEXTSIZE      | float  | Default text height                 |
+----------------+--------+-------------------------------------+
| $TEXTSTYLE     | string | Current text style name             |
+----------------+--------+-------------------------------------+
| $THICKNESS     | float  | Current thickness set by ELEV       |
|                |        | command                             |
+----------------+--------+-------------------------------------+
| $TILEMODE      | int    | 1 for previous release              |
|                |        | compatibility mode, 0 otherwise     |
+----------------+--------+-------------------------------------+
| $TRACEWID      | float  | Default Trace width                 |
+----------------+--------+-------------------------------------+
| $UCSNAME       | string | Name of current UCS                 |
+----------------+--------+-------------------------------------+
| $UCSORG        | 3DPoint| Origin of current UCS (in WCS)      |
|                |        |                                     |
+----------------+--------+-------------------------------------+
| $UCSXDIR       | 3DPoint| Direction of current UCS's X axis   |
|                |        | (in World coordinates)              |
+----------------+--------+-------------------------------------+
| $UCSYDIR       | 3DPoint| Direction of current UCS's Y axis   |
|                |        | (in World coordinates)              |
+----------------+--------+-------------------------------------+
| $UNITMODE      | int    | Low bit set = display fractions,    |
|                |        | feet-and-inches, and surveyor's     |
|                |        | angles in input format              |
+----------------+--------+-------------------------------------+
| $USERI1 - 5    | int    | Five integer variables intended     |
|                |        | for use by third-party developers   |
+----------------+--------+-------------------------------------+
| $USERR1 - 5    | float  | Five real variables intended        |
|                |        | for use by third-party developers   |
+----------------+--------+-------------------------------------+
| $USRTIMER      | int    | 0 = timer off, 1 = timer on         |
+----------------+--------+-------------------------------------+
| $VISRETAIN     | int    | 0 = don't retain Xref-dependent     |
|                |        | visibility settings, 1 = retain     |
|                |        | Xref-dependent visibility settings  |
+----------------+--------+-------------------------------------+
| $WORLDVIEW     | int    | 1 = set UCS to WCS during           |
|                |        | DVIEW/VPOINT, 0 = don't change UCS  |
+----------------+--------+-------------------------------------+