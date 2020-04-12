import circle_fit as cf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_circles

fig, ax = plt.subplots()
ax.set_aspect(1)

coords = [[1,0],[0.7,0.7],[0.866,0.5],[0.5,0.866],[0,1]]
print(coords)

plt.scatter([i[0] for i in coords], [i[1] for i in coords])


# FIT CIRCLE 
xc,yc,r,s = cf.hyper_fit(coords)
print(f'{xc} : {yc} : {r} : {s}')

# PLOT CIRCLE
circle1 = plt.Circle((xc, yc), r, linestyle='--', fill=False)
ax.add_artist(circle1)

# FORMULATE G CODE COMMAND
print(f"{xc}, {yc}, {r}, {s}")
print(f"G2 X{coords[-1][0]} Y{coords[-1][1]} R{round(r, 5)}")

# SHOW PLOT
plt.show()