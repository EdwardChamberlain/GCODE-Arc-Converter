import gcode_utils
import circle_fit as cf

print("\nTEST: contains_letter()")
cases = [
    {
        'case': "1234",
        'result': False
    },
    {
        'case': "1234A",
        'result': True
    },
    {
        'case': "AB",
        'result': True
    },
    {
        'case': "ab",
        'result': True
    },
    {
        'case': "1234aB",
        'result': True
    }
]
for s in cases:
    print(s, end=" : ")
    if gcode_utils.contains_letters(s['case']) == s['result']:
        print("PASS")
    else:
        print("FAIL")


print("\nTEST: parse_gcode()")
cases = [
    {
        'case': "G1 F1 X2 Y3 E4",
        'result': {
            'G': 1,
            'F': 1.0,
            'X': 2.0,
            'Y': 3.0,
            'E': 4.0,
            'Z': None
        }
    },
    {
        'case':"G0",
        'result': {
            'G': 0,
            'F': None,
            'X': None,
            'Y': None,
            'E': None,
            'Z': None
        }
    },
    {
        'case': "G1 X5",
        'result': {
            'G': 1,
            'F': None,
            'X': 5,
            'Y': None,
            'E': None,
            'Z': None
        }
    },
    {
        'case': "G1 X5 Y'Hello' Z5",
        'result': {
            'G': 1,
            'F': None,
            'X': 5,
            'Y': "'Hello'",
            'E': None,
            'Z': 5
        }
    }
]
for s in cases:
    print(s, end=" : ")
    if gcode_utils.parse_gcode(s['case']) == s['result']:
        print("PASS")
    else:
        print("!!! FAIL !!!")
        print(gcode_utils.parse_gcode(s['case']))


print("\nTEST: build_g_move()")
cases = [
    {
        'case': {'G': 1, 'X': 88.672, 'Y': 89.062, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59},
        'result': "G1 X88.672 Y89.062 E0.01284"
    }
]
for s in cases:
    print(s, end=" : ")
    if gcode_utils.build_g_move(s['case']) == s['result']:
        print("PASS")
    else:
        print("FAIL")