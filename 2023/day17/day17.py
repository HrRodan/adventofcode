import functools
import heapq
import math

import networkx as nx
import numpy as np
from itertools import pairwise

from utilities import tuple_add, POINT_TYP

with open('input.txt') as file:
    heat_loss_raw = [[int(x) for x in line.strip()] for line in file.readlines()]

shape = (len(heat_loss_raw), len(heat_loss_raw[0]))
# heat_loss = np.array(heat_loss_raw)
G_heat_loss = nx.DiGraph()
all_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
for i, line in enumerate(heat_loss_raw):
    for j, value in enumerate(line):
        position = (i, j)
        for d in all_directions:
            n1, n2 = tuple_add(position, d)
            if (0 <= n1 < shape[0] and 0 <= n2 < shape[1]):
                G_heat_loss.add_edge(position, (n1, n2), weight=heat_loss_raw[n1][n2], direction=d)

source = (0, 0)
target = (shape[0] - 1, shape[1] - 1)


@functools.lru_cache(5000)
def tuple_diff(t1: POINT_TYP, t2: POINT_TYP):
    return (t2[0] - t1[0], t2[1] - t1[1])

oint_direction_to_visit = []
# heap order: min(path_weight, count_direction, direction, position)
heapq.heappush(point_direction_to_visit, (0, 0, (0, 0), source))
# visited order (position, count_direction, direction : total_weight)
visited = {(source, 0, (0, 0)): 0}
min_heat = math.inf

# Dijkstra's algorithm
while point_direction_to_visit:
    # print(len(point_direction_to_visit))
    current_weight, current_direction_count, current_direction, current_position = heapq.heappop(
        point_direction_to_visit)
    for next_position, edge_dict in G_heat_loss[current_position].items():
        next_direction = edge_dict['direction']
        next_weight = current_weight + edge_dict['weight']
        # valid_next_position = True
        if next_direction == current_direction:
            next_direction_count = current_direction_count + 1
            if next_direction_count > 3:
                continue
        else:
            next_direction_count = 1
        if next_position == target:
            min_heat = min(min_heat, current_weight + edge_dict['weight'])
            continue
        # check for turn around
        if current_direction[0] == -next_direction[0] and current_direction[1] == -next_direction[1]:
            continue

        next_point_direction_tuple = (next_position, next_direction_count, next_direction)
        if next_point_direction_tuple in visited:
            previous_weight = visited[next_point_direction_tuple]
            if previous_weight <= next_weight:
                continue
        visited[next_point_direction_tuple] = next_weight
        heapq.heappush(point_direction_to_visit, (next_weight, next_direction_count, next_direction, next_position))

print(min_heat)

# part 2

point_direction_to_visit = []
# heap order: min(path_weight, count_direction, direction, position)
heapq.heappush(point_direction_to_visit, (0, 0, (0, 0), source))
# visited order (position, count_direction, direction : total_weight)
visited = {(source, 0, (0, 0)): 0}
min_heat = math.inf

# Dijkstra's algorithm
while point_direction_to_visit:
    current_weight, current_direction_count, current_direction, current_position = heapq.heappop(
        point_direction_to_visit)
    for next_position, edge_dict in G_heat_loss[current_position].items():
        next_direction = edge_dict['direction']
        next_weight = current_weight + edge_dict['weight']
        # valid_next_position = True
        if next_direction == current_direction or current_direction == (0, 0):
            next_direction_count = current_direction_count + 1
            if next_direction_count > 10:
                continue
        else:
            # allow turn only after min 4 steps
            if current_direction_count < 4:
                continue
            next_direction_count = 1
        # target can only be reached after at least 4 steps
        if next_position == target and next_direction_count < 4:
            continue
        # check for turn around
        if current_direction[0] == -next_direction[0] and current_direction[1] == -next_direction[1]:
            continue

        next_point_direction_tuple = (next_position, next_direction_count, next_direction)
        if next_point_direction_tuple in visited:
            previous_weight = visited[next_point_direction_tuple]
            if previous_weight <= next_weight:
                continue
        if next_position == target:
            min_heat = min(min_heat, current_weight + edge_dict['weight'])
            continue
        visited[next_point_direction_tuple] = next_weight
        heapq.heappush(point_direction_to_visit, (next_weight, next_direction_count, next_direction, next_position))

print(min_heat)

# 1104 too low
