#####################################
#                                   #
#          GCODE Utilities          #
#       By Edward Chamberlain       #
#                                   #
#####################################

import numpy as np
from alive_progress import alive_bar
import circle_fit as cf
import matplotlib.pyplot as plt
from itertools import groupby

DEBUG = False # ENABLES FULL DEBUG
PLOTTING = False # ENABLES PLOTTING OF GCODE (will create a large number of graphs)
Sthreshold = 0.0001 # THRESHOLD TO DETERMINE AN ARC
round_length = 6

def contains_letters(input_string):
    """
    Returns True if the string contains letters but false if it does not. Be careful with scientific notation floats.

    UNUSED: LIKELY TO BE REMOVED IMMINENTLY
    """

    transformed_string = input_string.lower()
    return transformed_string.islower()

def build_g_move(gcode):
    """
    Construts a GCode commands string from a GCode dicts.
    """

    # JOIN DICT TERMS TOGETHER EXCLUDING 'ln'
    result = " ".join(f"{k}{v}" for k, v in gcode.items() if (v != None and k != 'ln'))

    if DEBUG: print(result)

    return result

def parse_gcode(input_string):
    """
    Takes a string and parses it into a dict representing the move. 
    
    Only works for G moves and keys G, X, Y, Z, E, and F. GCode keys must be split by a space.
    """

    # SET KEYS TO COLLECT 
    keys = ["G", "X", "Y", "Z", "R", "E", "F"]

    # CREATE A ZEROD DICT TO STORE RESULTS
    result = {key: None for key in keys}

    # CONVERT STRING TO DICT - REQUIRES SPACED GCODE
    for elem in input_string.split():
        for key in keys: 
            if elem.startswith(key):
                value = elem[1:]
                try:
                    if key == "G":
                        result[key] = int(value)
                    else:
                        result[key] = float(value)
                except ValueError:
                    result[key] = value
            
    return result

def parse_gcode_batch(input_list):
    '''
    Takes in a list of strings and parses them into GCODE.
    '''

    # INITILISE LIST
    parsed_list = []

    print("Parsing GCode:")

    # PARSE EACH LINE OF CODE
    with alive_bar(len(input_list)) as bar:
        for index, i in enumerate(input_list):
            if i[:1] == "G":
                parsed_line = parse_gcode(i)
                parsed_line['ln'] = index
                if DEBUG: print(f"'{i[:-1]}'' -> {parsed_line}")
                parsed_list.append(parsed_line)
            bar()
    print(f"Parsed {len(parsed_list)} lines.")

    return parsed_list

def read_gcode_file(filename):
    """
    Opens a specified file and returns a GCode dict.
    """

    print(f"Loading '{filename}'...", end=" ")

    # OPEN AND READ FILE
    f = open(filename, 'r')
    GCODE = f.readlines()
    f.close()

    print(f"Done! {len(GCODE)} lines.")

    # STRIP NEW LINES
    GCODE = [line.rstrip("\n") for line in GCODE]

    # CONVERT TO LIST OF DICTS
    parsed_file = parse_gcode_batch(GCODE)

    return parsed_file, GCODE

def fit_circle(gcode):
    """
    Takes a list of GCode commands in dict form and uses the least squares method to fit a cirlce. Returns xc, yx, r, s.
    """

    # PULL X Y COORDS
    coords = [[s['X'], s['Y']] for s in gcode] 

    # FIT CIRCLE 
    xc,yc,r,s = cf.least_squares_circle(coords)

    if DEBUG: print(f"CIRCLE FITTED:\n    X: {xc},\n    Y: {yc},\n    R: {r},\n    S: {s}")

    return xc, yc, r, s

def is_arc(gcode):
    """
    Takes a list of GCode commands in dict form and returns True if the list of points form a perfect arc.
    """

    # FIT CIRCLE TO POINTS
    xc, yc, r, s = fit_circle(gcode)

    if s < Sthreshold:
        return True
    else:
        return False

def extract_g_moves(gcode, move_type):
    '''
    Strips out all gcode moves of a certain type. e.g. G1 / G2 / G3.
    '''

    result = []

    for i in gcode:
        if i['G'] == move_type:
            if i['X'] is not None and i['Y'] is not None:
                result.append(i)

    if DEBUG: print(f"Extracted {len(result)} lines of G{move_type} moves")

    return result

def find_arc_indexs(gcode):
    '''
    Finds all arcs in a list of GCode moves.
    '''

    # SET SCAN PARAMETERS
    initial_scan_length = 5
    i = 0
    SCAN = True

    # INIT RESULT
    results = []

    print("Scanning for Arcs:")

    # SCAN FOR ARCS
    with alive_bar(manual=True) as bar:
        while SCAN:

            if DEBUG: print(f"AT INDEX: {i}")

            if check_arc(gcode[i:i+initial_scan_length]):
                
                if DEBUG: print("ARC FOUND")

                # EXPAND THE ARC
                expanded_arc = expand_arc(gcode, i)

                if DEBUG: print(f"Expanded Arc: {expanded_arc}")

                # MOVE TO ARC END
                i = expanded_arc['STOP']

                # ADD ARC TO RESULTS
                results.append(expanded_arc)

            else:
                if DEBUG: print("NO ARC")

            # INCREMENT i
            i = i + 1

            # DETERMINE WHETHER TO CONTINUE
            if i+initial_scan_length >= len(gcode):

                # END SCANNING
                SCAN = False
                i = len(gcode)
            
            # SET PROGRESS BAR
            bar(i / len(gcode))
    
    print(f"Found {len(results)} Arcs:")

    return results 

def expand_arc(gcode, start_point):
    '''
    Takes in GCode and a starting index and calcualtes how long the arc is from that point.
    '''

    # SET INITIAL PARAMETERS
    scan_length = 5
    SEARCH = True
    arc_length = 0

    while SEARCH:
        # CALCUALTE ARC END POINT
        end_index = start_point+arc_length+scan_length

        if DEBUG: print(f"ARC TO TEST: START: {start_point}, END: {end_index}, LEN: {len(gcode[start_point : end_index])}")

        # CHECK IF RANGE IS NO LONGER AN ARC
        if not check_arc(gcode[start_point : end_index]):

            if DEBUG: print("---- END OF ARC ----")

            # END SEARCH
            SEARCH = False

        else:

            if not end_index >= len(gcode):

                # INCREMENT ARC LENGTH AND CHECK AGAIN
                arc_length = arc_length + 1

            else:

                # END SEARCH
                SEARCH = False

        # plot_gcode(gcode[start_point:end_index])

    # COMPENSATE ARC LENGTH DUE TO OVERSHOOT
    arc_length_comp = arc_length + scan_length - 2

    return {'START': start_point, 'STOP': arc_length_comp+start_point}

def plot_gcode_arc(points, start, end, plot_title="Gcode Plot"):
    '''
    Plots a GCode file and the arc found between start and end.
    '''

    # EXTRACT COORDS
    coords = [[s['X'], s['Y']] for s in points] 

    # CREATE FIGURE
    fig, ax = plt.subplots()
    ax.set_aspect(1)
    ax.set_title(plot_title)

    # PLOT SCATTER POINTS
    plt.scatter([i[0] for i in coords], [i[1] for i in coords])

    # FIT CIRCLE 
    xc,yc,r,s = fit_circle(points[start:end+1])

    # PLOT CIRCLE
    circle1 = plt.Circle((xc, yc), r, linestyle='--', fill=False)
    ax.add_artist(circle1)

    # SHOW PLOT
    plt.show()

def build_arc_move(gcode):
    '''
    Produces a G2 / G3 arc command for an input of GCode.
    '''

    # FIT CIRCLE 
    xc,yc,r,s = fit_circle(gcode)

    if DEBUG: print(f"CIRCLE FITTED:\n    X: {xc},\n    Y: {yc},\n    R: {r},\n    S: {s}")

    # DETERMINE MOVE TYPE
    movetype = move_type(gcode, (xc, yc))

    # SUM E TOTAL
    E_total = sum(i['E'] for i in gcode[1:] if i['E'] is not None)

    # FIND CENTERPOINT
    x_center = xc - gcode[0]['Y']
    y_center = yc - gcode[0]['X']

    # FORMULATE G CODE COMMAND
    if s < Sthreshold:
        COMMAND = f"{movetype} X{round(gcode[-1]['X'], round_length)} Y{round(gcode[-1]['Y'], round_length)} I{round(x_center, round_length)} J{round(y_center, round_length)} E{round(E_total, round_length)}"
        
        if gcode[1]['F'] is not None:
            COMMAND = COMMAND + (f" F{gcode[1]['F']}")

        if DEBUG: print(f'{round(s, round_length)} : {COMMAND}')
        return COMMAND
    else:
        print(f"{round(s, 5)} > {Sthreshold} : NOT AN ARC MOVE")

def move_type(gcode, centre):
    '''
    Receives an arc of G1 moves and returns whether it is clockwise or anti-clockwise in the format G2 / G3.
    '''

    # PULL X Y COORDS
    coords = [[s['X'], s['Y']] for s in gcode] 

    # DEFINE TWO POINTS
    p1 = (coords[0][0], coords[0][1])
    p2 = (coords[1][0], coords[1][1])

    # CALCUALTE VECTORs FROM CENTER OF CIRCLE TO POINTS
    v1 = [p1[0] - centre[0], p1[1] - centre[1]]
    v2 = [p2[0] - centre[0], p2[1] - centre[1]]

    # CROSS PRODUCT TO DETERMINE ANGLE
    if np.cross(v1, v2) > 0:
        return "G3"
    else: 
        return "G2"

def get_line_number(gcode):
    '''
    Takes a single GCode command and returns the line number of the file
    '''

    return gcode['ln']

# --------------------- NON CONFIRMED ---------------------

def replace_move(command, raw_file, arc):
    print("NOT IMPLENTED")

def replace_gcode_with_arcs():
    print("NOT IMPLEMENTED")

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

def print_gcode(gcode):
    for i in gcode:
        print(i)

def plot_gcode(points, plot_title="GCode Plot"):

    coords = [[s['X'], s['Y']] for s in points] 

    # CREATE FIGURE
    fig, ax = plt.subplots()
    ax.set_aspect(1)
    ax.set_title(plot_title)
    #ax.set_xlim([-50,50])
    #ax.set_ylim([-50,50])

    # PLOT SCATTER POINTS
    plt.scatter([i[0] for i in coords], [i[1] for i in coords], marker="o")

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

    print("Scanning for Arcs:")
    with alive_bar(manual=True) as bar:
        while SCAN:
            print(f"AT INDEX: {i}")

            if check_arc(gcode[i:i+initial_scan_length]):
                print("ARC FOUND")

                expand_arc(gcode, i)
                expanded_arc = expand_arc(gcode, i)
                results.append(expanded_arc)
                i = expanded_arc['STOP']
            else:
                print("NO ARC")

            if not i+initial_scan_length >= len(gcode):
                i = i + 1
            else:
                SCAN = False
            
            bar((i+1)/len(gcode))
    
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