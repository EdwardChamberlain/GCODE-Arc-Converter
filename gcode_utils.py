import numpy as np
from alive_progress import alive_bar
import circle_fit as cf
import matplotlib.pyplot as plt
from itertools import groupby

DEBUG = False
PLOTTING = False
Sthreshold = 0.0001

def extract_g_moves(gcode, move_type):
    result = []
    for i in gcode:
        if i['G'] == move_type:
            result.append(i)
    return result

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

    GCODE = [line.rstrip("\n") for line in GCODE]

    parsed_file = []

    print(f" Parsing: {filename}:")
    with alive_bar(len(GCODE)) as bar:
        for index, i in enumerate(GCODE):
            if i[:1] == "G":
                parsed_line = parse_gcode(i)
                parsed_line['ln'] = index
                if DEBUG: print(f"'{i[:-1]}'' -> {parsed_line}")
                parsed_file.append(parsed_line)
            bar()

    print(f" IMPORTED {len(parsed_file)} points")
    return parsed_file, GCODE

def move_type(p1, p2, centre):

    v1 = [p1[0] - centre[0], p1[1] - centre[1]]
    v2 = [p2[0] - centre[0], p2[1] - centre[1]]

    if np.cross(v1, v2) > 0:
        return "G3"
    else: 
        return "G2"

def compute_arc_move(points):

    # PULL X Y COORDS
    coords = [[s['X'], s['Y']] for s in points] 

    # FIT CIRCLE 
    xc,yc,r,s = cf.least_squares_circle(coords)
    if DEBUG: print(f"CIRCLE FITTED:\n    X: {xc},\n    Y: {yc},\n    R: {r},\n    S: {s}")

    # DETERMINE MOVE TYPE
    movetype = move_type(coords[0][:2], coords[1][:2], (xc, yc))

    # SUM E TOTAL
    E_total = sum([i['E'] for i in points])

    # FORMULATE G CODE COMMAND
    if s < Sthreshold:
        COMMAND = f"{movetype} X{coords[-1][0]} Y{coords[-1][1]} R{round(r, 5)} E{round(E_total, 5)}"
        if DEBUG: print(f'{round(s, 5)} : {COMMAND}')
        return COMMAND
    else:
        print(f"{round(s, 5)} : NOT AN ARC MOVE")


    # ------------- PLOTTING --------------
    # ASK TO PLOT
    #if input("PLOT FIGURE? (y/n): ") == "y":
    if PLOTTING:
        # CREATE FIGURE
        fig, ax = plt.subplots()
        ax.set_aspect(1)
        #ax.set_xlim([50,150])
        #ax.set_ylim([50,150])

        # PLOT SCATTER POINTS
        plt.scatter([i[0] for i in coords], [i[1] for i in coords])

        # PLOT CIRCLE
        circle1 = plt.Circle((xc, yc), r, linestyle='--', fill=False)
        ax.add_artist(circle1)

        # SHOW PLOT
        plt.show()

def plot_gcode(points):

    coords = [[s['X'], s['Y']] for s in points] 

    # CREATE FIGURE
    fig, ax = plt.subplots()
    ax.set_aspect(1)
    #ax.set_xlim([-50,50])
    #ax.set_ylim([-50,50])

    # PLOT SCATTER POINTS
    plt.scatter([i[0] for i in coords], [i[1] for i in coords])

    # SHOW PLOT
    plt.show()

def plot_gcode2(points, start, end):

    coords = [[s['X'], s['Y']] for s in points] 

    # CREATE FIGURE
    fig, ax = plt.subplots()
    ax.set_aspect(1)

    # PLOT SCATTER POINTS
    plt.scatter([i[0] for i in coords], [i[1] for i in coords])

    # PULL X Y COORDS
    coords = [[s['X'], s['Y']] for s in points[start:end]] 

    # FIT CIRCLE 
    xc,yc,r,s = cf.least_squares_circle(coords)

    # PLOT CIRCLE
    circle1 = plt.Circle((xc, yc), r, linestyle='--', fill=False)
    ax.add_artist(circle1)

    # SHOW PLOT
    plt.show()

def check_arc(points):
    # PULL X Y COORDS
    coords = [[s['X'], s['Y']] for s in points] 
    # print(f"no.points: {len(coords)}")

    # FIT CIRCLE 
    xc,yc,r,s = cf.least_squares_circle(coords)
    if DEBUG: print(f"CIRCLE FITTED:\n    X: {xc},\n    Y: {yc},\n    R: {r},\n    S: {s}")

    if s < Sthreshold:
        return True
    else:
        return False

def scan_for_arcs2(gcode):
    initial_scan_length = 5
    i = 0
    SCAN = True

    results = []

    while SCAN:
        # print(f"AT INDEX: {i}")

        if check_arc(gcode[i:i+initial_scan_length]):
            # print("ARC FOUND")
            expand_arc(gcode, i)
            expanded_arc = expand_arc(gcode, i)
            results.append(expanded_arc)
            i = expanded_arc['STOP']
        # else:
        #     # print("NO ARC")

        if not i+initial_scan_length >= len(gcode):
            i = i + 1
        else:
            SCAN = False
    
    return results 
  
def scan_for_arcs(gcode):
    # BUILD TRUTH TABLE FOR is_arc
    scan_length = 10
    is_arc = [check_arc(gcode[n:scan_length + n]) for n in range((len(gcode)-scan_length))]

    start = 0
    stop = 0

    results = []

    for value, grp in groupby(is_arc):
        grp = list(grp)
        stop += len(grp)
        if value == True: results.append({'START':start, 'STOP':stop - 1 + scan_length})
        start = stop

    # DEFINE ARCS
    computed_arcs = []
    for arc in results:
        computed_arcs.append(expand_arc(gcode, arc['START']))


    return computed_arcs

def expand_arc(gcode, start_point):

    scan_length = 5
    SEARCH = True
    arc_length = 0

    while SEARCH:
        end_index = start_point+arc_length+scan_length
        # print(f"LEN: {len(gcode[start_point : end_index])}, START: {start_point}, END: {end_index}")
        if not check_arc(gcode[start_point : end_index]):
            # print("----END OF ARC")
            SEARCH = False
        else:
            if not end_index >= len(gcode):
                arc_length = arc_length + 1
            else:
                SEARCH = False
        # plot_gcode(gcode[start_point:end_index])

    arc_length_comp = arc_length + scan_length - 1

    return {'START': start_point, 'STOP': arc_length_comp+start_point}