import circle_fit as cf
import numpy as np
from alive_progress import alive_bar

import gcode_utils

# IMPORT GCODE
imported_file = gcode_utils.read_gcode_file("Sample.gcode")

# TRIM GCODE -  Converts into batches. 
batch_size = 30

for i in range(0, len(imported_file), batch_size):
    subList = [i for i in imported_file[i:(i+batch_size)]]
    gcode_utils.compute_arc_move(subList)