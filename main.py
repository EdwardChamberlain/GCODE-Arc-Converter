import circle_fit as cf
import matplotlib.pyplot as plt
import numpy as np

import gcode_utils

Sthreshold = 0.002

# IMPORT GCODE
imported_file = gcode_utils.read_gcode_file("Sample.gcode")

# PULL X Y COORDS
coords = [[s['X'], s['Y']] for s in imported_file] 

# TRIM GCODE - all points is likely too many, so running with less meakes more sense for now!
coords = coords[0:20] 

# FIT CIRCLE 
xc,yc,r,s = cf.hyper_fit(coords)
print(f"CIRCLE FITTED:\n    X: {xc},\n    Y: {yc},\n    R: {r},\n    S: {s}")

# DETERMINE MOVE TYPE
movetype = gcode_utils.move_type(coords[0][:2], coords[1][:2])

# SUM E TOTAL
E_total = sum([i['E'] for i in imported_file])

# FORMULATE G CODE COMMAND
if s < Sthreshold:
    print(f'GCODE:\n    "{movetype} X{coords[-1][0]} Y{coords[-1][1]} R{round(r, 5)} E{round(E_total, 5)}"')
else:
    print(f"GCODE:\n    NOT AN ARC MOVE")


# ------------- PLOTTING --------------
# CREATE FIGURE
fig, ax = plt.subplots()
ax.set_aspect(1)

# PLOT SCATTER POINTS
plt.scatter([i[0] for i in coords], [i[1] for i in coords])

# PLOT CIRCLE
circle1 = plt.Circle((xc, yc), r, linestyle='--', fill=False)
ax.add_artist(circle1)

# SHOW PLOT
plt.show()