from collections import namedtuple

DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
    "stay": (0, 0)
}

Position = namedtuple("Position", ["x", "y"])