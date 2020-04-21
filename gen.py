import gcode_utils
import numpy as np

# SET STARTING POINTS
coords = [
    {'G':1, 'X':0, 'Y':-15, 'E':0},
    {'G':1, 'X':15, 'Y':-15, 'E':0}
]

# CREATE PERFECT ARC MOVE
r = 15
for i in range(0, 91, 5):
    y = r * np.sin(np.deg2rad(i))
    x = r * np.cos(np.deg2rad(i))
    coords.append({'G':1, 'X':x, 'Y':y, 'E':0})

# APPEND FINSIHING MOVES
coords.append({'G':1, 'X':-15, 'Y':15, 'E':0})
coords.append({'G':1, 'X':-15, 'Y':0, 'E':0})

# CONVERT TO STRINGS
output = [gcode_utils.build_g_move(n) for n in coords]

# WRITE TO OUTPUT FILE
with open("gcode/gen_output.gcode", 'w') as f:
    for item in output:
        f.write("%s\n" % item)

# PLOT CREATED FILE
gcode_utils.plot_gcode(coords)