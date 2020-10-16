import os

t = "/home/pi/Documents/GCODE-Arc-Converter/gcode1.gcode"

def get_file_name(path):
    path = os.path.split(path)
    filename = path[0] + path[1].split('.')[0] + "_processed.gcode"
    return filename

print(get_file_name(t))