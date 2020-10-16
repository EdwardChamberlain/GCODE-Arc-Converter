import os

def get_file(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()


def get_marker_index(data, args):
    return [data.index(i) for i in args]


def insert_gcode_layer(host_file, insert_file, layer):
    host_start, host_end = get_marker_index(
        host_file,
        [f';LAYER:{layer}\n', f';LAYER:{layer+1}\n']
    )
    insert_start, insert_end = get_marker_index(
        insert_file,
        [f';LAYER:{layer}\n', f';LAYER:{layer+1}\n']
    )

    del host_file[host_start:host_end-1]

    host_file = host_file[:host_start] + insert_file[insert_start:insert_end-1] + host_file[host_start:]

    return host_file


def save_to_file(input_file, filepath):
    with open(filepath, 'w') as f:
        f.writelines(input_file)


def get_file_name(path_input):
    if path_input == "":
        path = os.path.split(path)
        path_input = path[0] + path[1].split('.')[0] + "_processed.gcode"
    return path_input


def process_replacement(host_filepath, insert_filepath, replacelayer=0, output_file=""):
    output_file = get_file_name(host_filepath)
        
    host_data = get_file(host_filepath)
    insert_data = get_file(insert_filepath)

    result = insert_gcode_layer(host_data, insert_data, replacelayer)

    save_to_file(result, output_file)


if __name__ == '__main__':
    host_in = input('3D Gcode: ')
    insert_in = input('Texture Gcode: ')

    process_replacement(host_in, insert_in, 0)
