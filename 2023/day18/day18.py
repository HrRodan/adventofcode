import numpy as np
from scipy.ndimage import binary_fill_holes
from shapely.geometry import Polygon

from utilities import tuple_add

with open('input.txt') as file:
    dig_map = [(x, int(y), c[1:-1]) for line in file.readlines() for x, y, c in [line.strip().split()]]

directions = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}
trench = {}
position = (0, 0)
for x, y, c in dig_map:
    for _ in range(y):
        position = tuple_add(position, directions[x])
        trench[position] = c

shift_value = tuple(-min(x) for x in zip(*trench.keys()))
trench = {tuple_add(x, shift_value): k for x, k in trench.items()}
shape = tuple(max(x) + 1 for x in zip(*trench.keys()))

trench_array = np.full(shape=shape, fill_value=False)
trench_array[tuple(np.transpose(tuple(trench.keys())))] = True
hole = binary_fill_holes(trench_array)
print(hole.sum())

# part 2
direction_map_p2 = {
    '0': directions['R'],
    '1': directions['D'],
    '2': directions['L'],
    '3': directions['U']
}
trench_edges_p2 = []
position = (0, 0)
for x, y, c in dig_map:
    direction = direction_map_p2[c[-1]]
    count_per_direction = int(c[1:-1], 16)
    position = tuple_add(position, tuple(np.multiply(direction, count_per_direction)))
    trench_edges_p2.append(position)

polygon = Polygon(trench_edges_p2)
# each polygon has 4 outside edges more than inside edges
# each point on edge contribues 1/2 on average
# 4 outside points contribute 4 * 3/4
print(int(polygon.area+(polygon.length-4)/2+3))
