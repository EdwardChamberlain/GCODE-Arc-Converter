import circle_fit as cf
import matplotlib.pyplot as plt
import numpy as np

import Gcode_utils

# IMPORT GCODE
coords = Gcode_utils.readGCODE("Sample.gcode")

# TRIM GCODE
coords = coords[0:20]

# CREATE FIGURE
fig, ax = plt.subplots()
ax.set_aspect(1)
plt.scatter([i[0] for i in coords], [i[1] for i in coords])

# FIT CIRCLE 
xc,yc,r,s = cf.hyper_fit(coords)
print(f"CIRCLE: {xc}, {yc}, {r}, {s}")

# PLOT CIRCLE
circle1 = plt.Circle((xc, yc), r, linestyle='--', fill=False)
ax.add_artist(circle1)

# Find move type
movetype = Gcode_utils.move_type(coords[0], coords[1])

# FORMULATE G CODE COMMAND
print(f" GCODE: {movetype} X{coords[-1][0]} Y{coords[-1][1]} R{round(r, 5)}")

# SHOW PLOT
plt.show()