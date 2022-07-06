import math


CIRLCE_RAD = 5

# GENERATE AN SEMI CIRCLE
points = [
    (
        CIRLCE_RAD * math.sin(math.radians(i)),
        CIRLCE_RAD * math.cos(math.radians(i)),
        0,
    )
    for i in range(180)
]

# GENERATE A SQUARE SIDE
points.append(
    (
        - CIRLCE_RAD,
        - CIRLCE_RAD,
        0
    )
)

points.append(
    (
        - CIRLCE_RAD,
        CIRLCE_RAD,
        0
    )
)

points.append(
    (
        0,
        CIRLCE_RAD,
        0
    )
)

# GENERATE GCODE POINTS
GCode = [
    f"G0 X{p[0]} Y{p[1]} Z{p[2]}"
    for p in points
]
GCode[0] += " F100"

# SAVE OUTPUT
with open("sample.gcode", 'w') as f:
    f.write('\n'.join(GCode))

# SHOW OUTPUT
if False:
    import matplotlib.pyplot as plt

    x = [i[0] for i in points]
    y = [i[1] for i in points]
    plt.plot(x, y, 'x-')
    plt.axis('equal')
    plt.show()
