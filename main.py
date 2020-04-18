import circle_fit as cf
import numpy as np
from alive_progress import alive_bar

import gcode_utils

INPUT_FILE = "gcode/skin.gcode"
OUTPUT_FILE = "Output.gcode"

# IMPORT GCODE
parsed_file, gcode_file = gcode_utils.read_gcode_file(INPUT_FILE)

# STRIP NON G1 MOVES
trimmed_data = []
for i in parsed_file:
    if i['G'] == 1:
        trimmed_data.append(i)

# GET ARC LOCATIONS
found_arcs = gcode_utils.scan_for_arcs(trimmed_data)

print(f"{len(found_arcs)} Arcs found!")

# GENERATE ARCS FOR FOUND ARCS
for arc in found_arcs:
    # GET ARC
    COMMAND = gcode_utils.compute_arc_move(trimmed_data[arc['START']:arc['STOP']])

    # GET LN NUMBER
    LINE = {'START':trimmed_data[arc['START']]['ln'], 'STOP':trimmed_data[arc['STOP']]['ln']}

    # REposition FILE INFO
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