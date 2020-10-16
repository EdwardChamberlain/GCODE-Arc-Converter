import PySimpleGUI as sg
import Code_Splicer

sg.theme('Black')
layout = [
    [sg.T("3D GCODE", size=(14, None)), sg.In(key='3d_filepath'), sg.FileBrowse(target='3d_filepath')],
    [sg.T("Texture GCODE", size=(14, None)), sg.In(key='texture_filepath'), sg.FileBrowse(target='texture_filepath')],
    [sg.Button('Process'), sg.T("", key='result', size=(30,None))]
]

win = sg.Window('Test', layout)

# EVENTS
def btn_process(event, values):
    win['result'].Update("Processing")
    Code_Splicer.process_replacement(values['3d_filepath'], values['texture_filepath'])
    win['result'].Update("Done!")

events = {'Process': btn_process}

while True:
    event, values = win.read()
    if event == sg.WIN_CLOSED:
        break
    
    events[event](event, values)