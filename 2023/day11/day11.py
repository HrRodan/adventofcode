from itertools import combinations

import numpy as np

from utilities import POINT_TYP

with open('input.txt') as file:
    galaxy_raw = np.array([list(line.strip()) for line in file.readlines()])

galaxy = galaxy_raw == '#'
galaxy_points = np.transpose(np.nonzero(galaxy))
empty_rows = np.flatnonzero(np.logical_not(np.any(galaxy, axis=1)))
empty_columns = np.flatnonzero(np.logical_not(np.any(galaxy, axis=0)))


def get_distance(p1: POINT_TYP, p2: POINT_TYP, emtpy_row_factor=2):
    (x1, y1), (x2, y2) = p1, p2
    x_sorted = sorted([x1, x2])
    y_sorted = sorted([y1, y2])
    base_distance = (x_sorted[1] - x_sorted[0]) + (y_sorted[1] - y_sorted[0])
    dx = sum(x_sorted[0] < x < x_sorted[1] for x in empty_rows)
    dy = sum(y_sorted[0] < y < y_sorted[1] for y in empty_columns)
    return base_distance + (dx + dy) * (emtpy_row_factor - 1)


result = sum(get_distance(p1, p2) for p1, p2 in combinations(galaxy_points, 2))
print(result)

result_part2 = sum(get_distance(p1, p2, 1000000) for p1, p2 in combinations(galaxy_points, 2))
print(result_part2)
