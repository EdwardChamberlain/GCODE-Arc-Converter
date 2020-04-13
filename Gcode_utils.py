import numpy as np

def parse_gcode(input):
    keys = ["X", "Y", "Z", "E"]
    X_VAL = 0
    Y_VAL = 0
    Z_VAL = 0
    E_VAL = 0
    for elem in input.split():
        if elem.startswith(keys[0]):
            X_VAL = float(elem[1:])
        if elem.startswith(keys[1]):
            Y_VAL = float(elem[1:])
        if elem.startswith(keys[2]):
            Z_VAL = float(elem[1:])
        if elem.startswith(keys[3]):
            E_VAL = float(elem[1:])

    return [X_VAL, Y_VAL, Z_VAL, E_VAL]


def read_gcode_file(filename):
    f = open(filename, 'r')
    GCODE = f.readlines()
    f.close()

    coords = []

    for i in GCODE:
        if i[:2] == "G1":
            print(f"{i[:-1]}", end=' -> ')

            parsed_line = parse_gcode(i)
            
            print(parsed_line)
 
            coords.append(parsed_line)

    print(f"IMPORTED {len(coords)} points")
    return coords

def move_type(p1, p2):

    v1 = p1
    v2 = p2

    if np.cross(v1, v2) > 0:
        return "G3"
    else: 
        return "G2"