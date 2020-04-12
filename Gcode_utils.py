import numpy as np

def readGCODE(filename):
    f = open('Sample.gcode', 'r')
    GCODE = f.readlines()
    f.close()

    coords = []

    for i in GCODE:
        if i[:2] == "G1":
            indexX = i.index("X")
            indexEndX = i[indexX:].index(" ") + indexX

            indexY = i.index("Y")
            indexEndY = i[indexY:].index(" ") + indexY

            coords.append([float(i[indexX+1:indexEndX]), float(i[indexY+1:indexEndY])])

    print(f"IMPORTED {len(coords)} points")

    return coords

def move_type(p1, p2):

    v1 = p1
    v2 = p2

    if np.cross(v1, v2) > 0:
        return "G3"
    else: 
        return "G2"