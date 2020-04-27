import gcode_utils as gcu

INPUT_FILE = "Output.gcode"

# IMPORT GCODE
parsed_file, gcode_file = gcu.read_gcode_file(INPUT_FILE)

print(parsed_file[3])

# PLOT GCODE
gcu.plot_gcode(parsed_file, plot_title="Imported Gcode")

