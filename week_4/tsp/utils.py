import math
from collections import namedtuple


Point = namedtuple("Point", ['x', 'y'])


def length(point1: Point, point2: Point) -> float:
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
