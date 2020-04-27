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
    },
    {
        'case': "G1 X9.18485099360515e-16 Y15.0 E0",
        'result': {
            'G': 1,
            'F': None,
            'X': 9.18485099360515e-16,
            'Y': 15.0,
            'E': 0,
            'Z': None
        }
    }
]
for s in cases:
    print(s, end=" : ")
    if gcode_utils.parse_gcode(s['case']) == s['result']:
        print("PASS")
    else:
        print("!!! FAIL !!!")
        print("   --> ", gcode_utils.parse_gcode(s['case']))


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

print("\nTEST: fit_circle()")
cases = [
    {
        'case': [{'G': 1, 'X': 5, 'Y': 0, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 0, 'Y': 5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': -5, 'Y': 0, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 0, 'Y': -5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}],
        'result': (0, 0, 5, 0)
    }
]
for s in cases:
    print(s, end=" : ")
    if gcode_utils.fit_circle(s['case']) == s['result']:
        print("PASS")
    else:
        print("FAIL", end=" : ")
        print(gcode_utils.fit_circle(s['case']))


print("\nTEST: is_arc()")
cases = [
    {
        'case': [{'G': 1, 'X': 5, 'Y': 0, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 0, 'Y': 5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': -5, 'Y': 0, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 0, 'Y': -5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}],
        'result': True
    },
    {
        'case': [{'G': 1, 'X': 4.5, 'Y': 0, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 0, 'Y': 5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': -5, 'Y': 0, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 0, 'Y': -5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}],
        'result': False
    }
]
for s in cases:
    print(s, end=" : ")
    if gcode_utils.is_arc(s['case']) == s['result']:
        print("PASS")
    else:
        print("FAIL", end=" : ")
        print(gcode_utils.fit_circle(s['case']))

print("\nTEST: move_type()")
cases = [
    {
        'case': [{'G': 1, 'X': 15, 'Y': 0, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 15, 'Y': 0.5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 15, 'Y': 1, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 15, 'Y': 1.5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59},{'G': 1, 'X': 15, 'Y': 2, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}],
        'result': "G3"
    },
    {
        'case': [{'G': 1, 'X': 15, 'Y': 0, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 15, 'Y': -0.5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 15, 'Y': -1, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}, {'G': 1, 'X': 15, 'Y': -1.5, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59},{'G': 1, 'X': 15, 'Y': -2, 'Z': None, 'E': 0.01284, 'F': None, 'ln': 59}],
        'result': "G2"
    }
]
for s in cases:
    print(s, end=" : ")
    if gcode_utils.move_type(s['case'], (0,0)) == s['result']:
        print("PASS")
    else:
        print("FAIL", end=" : ")
        print(gcode_utils.move_type(s['case']))