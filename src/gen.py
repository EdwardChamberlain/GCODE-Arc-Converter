import gcode_utils
import numpy as np

# SET STARTING POINTS
coords = [
    {'G':1, 'X':0, 'Y':-50, 'E':0},
    {'G':1, 'X':50, 'Y':-50, 'E':0}
]

# CREATE PERFECT ARC MOVE
r = 50
for i in range(0, 91, 5):
    y = r * np.sin(np.deg2rad(i))
    x = r * np.cos(np.deg2rad(i))
    coords.append({'G':1, 'X':x, 'Y':y, 'E':0})

# APPEND FINSIHING MOVES
coords.append({'G':1, 'X':-50, 'Y':50, 'E':0})
coords.append({'G':1, 'X':-50, 'Y':0, 'E':0})

# MOVE ORIGIN TO FRONT LEFT CORNER
for move in coords:
    move['X'] = move['X']+100
    move['Y'] = move['Y']+100

# CONVERT TO STRINGS
output = [gcode_utils.build_g_move(n) for n in coords]

# WRITE TO OUTPUT FILE
with open("gcode/gen_output.gcode", 'w') as f:
    for item in output:
        f.write("%s\n" % item)

# PLOT CREATED FILE
gcode_utils.plot_gcode(coords)