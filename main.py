print("Starting GCode Arc Converter...")

import circle_fit as cf
import numpy as np
from alive_progress import alive_bar
import os

import gcode_utils as gcu

OUTPUT_FILE = "Output.gcode"
PLOTTING = False

# TAKE INPUT
INPUT_FILE = input("File to process (path relative to install): ")
if not os.path.isfile(INPUT_FILE):
    input("ERROR: FILE NOT FOUND. PRESS ANY KEY TO EXIT")
    exit()

# IMPORT GCODE
parsed_file, gcode_file = gcu.read_gcode_file(INPUT_FILE)

# PLOT GCODE
if PLOTTING: gcu.plot_gcode(parsed_file, plot_title="Imported Gcode")

# GET G1 MOVES
trimmed_data = gcu.extract_g_moves(parsed_file, 1)

# EXTRACT ARCS
arcs_indexs = gcu.find_arc_indexs(trimmed_data)

# PLOT THE FOUND ARCS
if PLOTTING: 
    for i in arcs_indexs:
        gcu.plot_gcode_arc(trimmed_data, i['START'], i['STOP'], plot_title="Arc Found!")

with open("test1.gcode", 'w') as f:
    for item in gcode_file:
        f.write("%s\n" % item)

# CREATE PROGRESS BAR
print("Implementing Arcs:")
with alive_bar(len(arcs_indexs)) as bar:

    # CREATE THE GCODE COMMAND FOR THE ARC
    for arc in arcs_indexs:
        Arc_command = gcu.build_arc_move(trimmed_data[arc['START'] : arc['STOP'] + 1])

        # GET LINE NUMBER
        start_ln = gcu.get_line_number(trimmed_data[arc['START']])
        end_ln = gcu.get_line_number(trimmed_data[arc['STOP']])

        # REPLACE LINES start+1 TO END
        for line in range(start_ln + 1, end_ln + 1):
            gcode_file[line] = "# CONVERTED TO ARC"

        # ADD IN ARC
        gcode_file[start_ln+1] = Arc_command

        bar()

with open("test2.gcode", 'w') as f:
    for item in gcode_file:
        f.write("%s\n" % item)

# TIDY UP
output_list = []
for line in gcode_file:
    if line != "# CONVERTED TO ARC":
        output_list.append(line)

# OUTPUT FILE
with open(OUTPUT_FILE, 'w') as f:
    for item in output_list:
        f.write("%s\n" % item)

print(f"Complete! Output created: {OUTPUT_FILE}")