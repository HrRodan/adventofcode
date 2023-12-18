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


def count_visited_tiles(start_position: POINT_TYP, start_direction: POINT_TYP):
    all_visited_position_direction = set()

    def follow_beam(start: POINT_TYP, direction: POINT_TYP):
        position = tuple_add(start, direction)
        if not (0 <= position[0] < cave_shape[0] and 0 <= position[1] < cave_shape[1]):
            return False
        position_direction_tuple = (position, direction)
        if position_direction_tuple in all_visited_position_direction:
            return True
        all_visited_position_direction.add(position_direction_tuple)
        position_value = cave_raw[position]
        if position_value == '.':
            follow_beam(position, direction)
        elif direction[0] == 0:
            if position_value == '\\':
                follow_beam(position, TURN_RIGHT[direction])
            elif position_value == '/':
                follow_beam(position, TURN_LEFT[direction])
            elif position_value == '|':
                follow_beam(position, TURN_LEFT[direction])
                follow_beam(position, TURN_RIGHT[direction])
            elif position_value == '-':
                follow_beam(position, direction)
        elif direction[1] == 0:
            if position_value == '\\':
                follow_beam(position, TURN_LEFT[direction])
            elif position_value == '/':
                follow_beam(position, TURN_RIGHT[direction])
            elif position_value == '-':
                follow_beam(position, TURN_LEFT[direction])
                follow_beam(position, TURN_RIGHT[direction])
            elif position_value == '|':
                follow_beam(position, direction)
        else:
            return False

    follow_beam(start_position, start_direction)
    return len({x for x, _ in all_visited_position_direction})


print(count_visited_tiles((0, -1), (0, 1)))

# part 2
start_directions = ([t for x in range(cave_shape[1]) for t in [((-1, x), (1, 0)), ((cave_shape[0], x), (-1, 0))]] +
                    [k for y in range(cave_shape[0]) for k in [((y, -1), (0, 1)), ((y, cave_shape[1]), (0, -1))]])
