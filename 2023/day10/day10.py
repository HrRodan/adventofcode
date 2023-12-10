from collections import defaultdict

import networkx as nx
import numpy as np
from scipy import ndimage
from matplotlib.path import Path

with open('input.txt') as file:
    pipes = [line.strip() for line in file.readlines()]

pip_network = nx.Graph()
shape = (len(pipes), len(pipes[0]))
start = None
pipe_dict = {}
for i, row in enumerate(pipes):
    for j, pipe_value in enumerate(row):
        pipe_location = (i, j)
        north = (i - 1, j)
        south = (i + 1, j)
        east = (i, j + 1)
        west = (i, j - 1)
        match pipe_value:
            case 'S':
                start = pipe_location
            case '|':
                pipe_dict[pipe_location] = {north, south}
            case '-':
                pipe_dict[pipe_location] = {west, east}
            case 'L':
                pipe_dict[pipe_location] = {north, east}
            case 'J':
                pipe_dict[pipe_location] = {north, west}
            case '7':
                pipe_dict[pipe_location] = {south, west}
            case 'F':
                pipe_dict[pipe_location] = {south, east}
            case '.':
                pipe_dict[pipe_location] = set()

start_connections = {p for p, c in pipe_dict.items() if start in c}
pipe_dict[start] = start_connections

# follow_path
loop = {start}
ordered_loop = [start]
current_position = list(pipe_dict[start])[0]
loop.add(current_position)
ordered_loop.append(current_position)
while current_position != start:
    try:
        p = (pipe_dict[current_position] - loop).pop()
    except KeyError:
        p = start
    loop.add(p)
    ordered_loop.append(p)
    current_position = p

print(round(len(loop) / 2))

# %%
loop_path = Path(ordered_loop)

image_array = np.full(shape, False)
image_array[tuple(zip(*list(loop)))] = True
holes = np.logical_xor(image_array, ndimage.binary_fill_holes(image_array))
holes_as_points = np.transpose(np.nonzero(holes))
holes_in_path = loop_path.contains_points(holes_as_points)
print(sum(holes_in_path))
