import circle_fit as cf
import numpy as np
from alive_progress import alive_bar

import gcode_utils

# IMPORT GCODE
imported_file, GCODE_FILE = gcode_utils.read_gcode_file("skin.gcode")

# gcode_utils.plot_gcode(imported_file)

# STRIP NON G1 MOVES
trimmed_data = []
for i in imported_file:
    if i['G'] == 1:
        trimmed_data.append(i)
gcode_utils.plot_gcode(trimmed_data)

# GET ARC LOCATIONS
found_arcs = gcode_utils.scan_for_arcs(trimmed_data)

# GENERATE ARCS FOR FOUND ARCS
for i in found_arcs:
    # GET ARC
    COMMAND = gcode_utils.compute_arc_move(trimmed_data[i['START']:i['STOP']])

    # GET LN NUMBER
    LINE = {'START':trimmed_data[i['START']]['ln'], 'STOP':trimmed_data[i['STOP']]['ln']}
    
    print(f"i = {i} AT: {LINE}: {COMMAND}")

    # REPLACE FILE INFO
    for i in range(LINE['START'], LINE['STOP']):
        GCODE_FILE[i] = "# CONVERTED TO ARC"
    GCODE_FILE[LINE['START']] = COMMAND

with open('Output.txt', 'w') as f:
    for item in GCODE_FILE:
        f.write("%s\n" % item)