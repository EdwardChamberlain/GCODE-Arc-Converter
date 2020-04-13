import numpy as np
from alive_progress import alive_bar

DEBUG = False

def parse_gcode(input_string):
    # SET KEYS TO COLLECT 
    keys = ["G", "X", "Y", "Z", "E", "F"]

    # CREATE A ZEROD DICT TO STORE RESULTS
    result = {key: 0 for key in keys}

    for elem in input_string.split():
        for key in keys: 
            if elem.startswith(key):
                result[key] = float(elem[1:])
            
    return result


def read_gcode_file(filename):
    f = open(filename, 'r')
    GCODE = f.readlines()
    f.close()

    coords = []

    print(f" Parsing: {filename}:")
    with alive_bar(len(GCODE)) as bar:  # or a 1000 in the loop example.
        for i in GCODE:
            if i[:2] == "G1":
                
                parsed_line = parse_gcode(i)
                
                if DEBUG: print(f"{i[:-1]} -> {parsed_line}")
    
                coords.append(parsed_line)
            bar()

    print(f" IMPORTED {len(coords)} points")
    return coords

def move_type(p1, p2):

    v1 = p1
    v2 = p2

    if np.cross(v1, v2) > 0:
        return "G3"
    else: 
        return "G2"