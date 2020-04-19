import gcode_utils
import numpy as np

r = 15
coords = [
    {'G':1, 'X':0, 'Y':-15, 'E':0},
    {'G':1, 'X':15, 'Y':-15, 'E':0}
]

for i in range(0, 91, 5):
    y = r * np.sin(np.deg2rad(i))
    x = r * np.cos(np.deg2rad(i))
    coords.append({'G':1, 'X':x, 'Y':y, 'E':0})

coords.append({'G':1, 'X':-15, 'Y':15, 'E':0})
coords.append({'G':1, 'X':-15, 'Y':0, 'E':0})

for n in coords:
    gcode_utils.build_g_move(n)

gcode_utils.plot_gcode(coords)