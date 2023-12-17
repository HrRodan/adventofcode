import functools
import sys

import numpy as np
from utilities import tuple_add, POINT_TYP

sys.setrecursionlimit(10000)

with open('input.txt') as file:
    cave_raw = np.array([list(x.strip()) for x in file.readlines()])

cave_shape = cave_raw.shape

TURN_RIGHT = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}

TURN_LEFT = {v: k for k, v in TURN_RIGHT.items()}

all_empty = {tuple(x) for x in np.transpose(np.nonzero(cave_raw == '.'))}
all_vertical_splitters = {tuple(x) for x in np.transpose(np.nonzero(cave_raw == '|'))}
all_horizontal_splitters = {tuple(x) for x in np.transpose(np.nonzero(cave_raw == '-'))}
all_left_right_mirrors = {tuple(x) for x in np.transpose(np.nonzero(cave_raw == '/'))}
all_right_left_mirrors = {tuple(x) for x in np.transpose(np.nonzero(cave_raw == '\\'))}

all_visited_position_direction = set()
start_position = (0, -1)
start_direction = (0, 1)


def follow_beam(start: POINT_TYP, direction: POINT_TYP):
    position = tuple_add(start, direction)
    if not (0 <= position[0] < cave_shape[0] and 0 <= position[1] < cave_shape[1]):
        return False
    position_direction_tuple = (position, direction)
    if position_direction_tuple in all_visited_position_direction:
        return True
    all_visited_position_direction.add(position_direction_tuple)
    if position in all_empty:
        follow_beam(position, direction)
    elif direction[0] == 0:
        if position in all_right_left_mirrors:
            follow_beam(position, TURN_RIGHT[direction])
        elif position in all_left_right_mirrors:
            follow_beam(position, TURN_LEFT[direction])
        elif position in all_vertical_splitters:
            follow_beam(position, TURN_LEFT[direction])
            follow_beam(position, TURN_RIGHT[direction])
        elif position in all_horizontal_splitters:
            follow_beam(position, direction)
    elif direction[1] == 0:
        if position in all_right_left_mirrors:
            follow_beam(position, TURN_LEFT[direction])
        elif position in all_left_right_mirrors:
            follow_beam(position, TURN_RIGHT[direction])
        elif position in all_horizontal_splitters:
            follow_beam(position, TURN_LEFT[direction])
            follow_beam(position, TURN_RIGHT[direction])
        elif position in all_vertical_splitters:
            follow_beam(position, direction)
    else:
        return False


follow_beam(start_position, start_direction)
result = len({x for x, _ in all_visited_position_direction})
print(result)
