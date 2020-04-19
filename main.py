import circle_fit as cf
import numpy as np
from alive_progress import alive_bar

import gcode_utils

PLOT = False

INPUT_FILE = "gcode/skin.gcode"
OUTPUT_FILE = "Output.gcode"

# IMPORT GCODE
parsed_file, gcode_file = gcode_utils.read_gcode_file(INPUT_FILE)

# STRIP G1 MOVES
trimmed_data = gcode_utils.extract_g_moves(parsed_file, 1)

# PLOT IMPORTED AND TRIMMED GCODE
print("PLOTTING GCODE FILE")
if PLOT: gcode_utils.plot_gcode(parsed_file)
if PLOT: gcode_utils.plot_gcode(trimmed_data)

# GET ARC LOCATIONS
print("SCANNING FOR ARCS:")
found_arcs = gcode_utils.scan_for_arcs2(trimmed_data)

print(found_arcs)

if PLOT:
    for r in found_arcs:
        gcode_utils.plot_gcode(trimmed_data[r['START']:r['STOP']])
        gcode_utils.plot_gcode2(trimmed_data, r['START'], r['STOP'])

print(f"{len(found_arcs)} Arcs found!")

# GENERATE ARCS FOR FOUND ARCS
for arc in found_arcs:
    # GET ARC
    COMMAND = gcode_utils.compute_arc_move(trimmed_data[arc['START']:arc['STOP']])

    # GET LN NUMBER
    LINE = {'START':trimmed_data[arc['START']]['ln'], 'STOP':trimmed_data[arc['STOP']]['ln']}

    # Reposition FILE INFO
    for position in range(LINE['START'], LINE['STOP']):
        gcode_file[position] = "# CONVERTED TO ARC"
    gcode_file[LINE['START']] = COMMAND

# STRIP CONVERTED LINES
output_list = []
for line in gcode_file:
    if line != "# CONVERTED TO ARC":
        output_list.append(line)

with open(OUTPUT_FILE, 'w') as f:
    for item in output_list:
        f.write("%s\n" % item)

print(f"Complete! Output created: {OUTPUT_FILE}")