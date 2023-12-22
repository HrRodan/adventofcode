import networkx as nx
import numpy as np

with open('input.txt') as file:
    garden_map = np.array([list(x.strip()) for x in file.readlines()])

garden_map_original = garden_map.copy()
add_concat = 9

start_position = tuple(np.transpose(np.nonzero(garden_map == 'S'))[0])
start_position = (
start_position[0] + add_concat // 2 * garden_map.shape[0], start_position[1] + add_concat // 2 * garden_map.shape[1])

garden_map = np.concatenate([garden_map] * add_concat, axis=0)
garden_map = np.concatenate([garden_map] * add_concat, axis=1)

G_garden: nx.Graph = nx.grid_2d_graph(*garden_map.shape)
all_rocks = [tuple(x) for x in np.transpose(np.nonzero(garden_map == '#'))]
G_garden.remove_nodes_from(all_rocks)

all_positions = {start_position}
all_lengths = []
for _ in range(500):
    all_positions = {y for x in all_positions for y in G_garden[x]}
    all_lengths.append(len(all_positions))

print(all_lengths[63])

# %%part 2
# periodicity start at 65 (after one frame), then each frame (131)
# constant in 2nd derivative -> quadratic function
# start luckily exactly at center
offset = garden_map_original.shape[0] // 2
periodicity = garden_map_original.shape[0]
# function: y = (x - offset) ^ 2 valid for x element of multiple of 131
points = list(zip(*list(enumerate([0]+all_lengths, start=0))[offset::periodicity]))
# np.diff(points[1], n=2) = array([31134, 31134])
fct = np.polyfit(*points, 2)
# luckily the value of steps is exactly on the periodicity
result = np.polyval(fct, 26501365)
print(round(result))