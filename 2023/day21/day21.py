import networkx as nx
import numpy as np

with open('input.txt') as file:
    garden_map = np.array([list(x.strip()) for x in file.readlines()])

G_garden: nx.Graph = nx.grid_2d_graph(*garden_map.shape)
all_rocks = [tuple(x) for x in np.transpose(np.nonzero(garden_map == '#'))]
G_garden.remove_nodes_from(all_rocks)
start_position = tuple(np.transpose(np.nonzero(garden_map == 'S'))[0])

all_positions = {start_position}
for _ in range(64):
    all_positions = {y for x in all_positions for y in G_garden[x]}

print(len(all_positions))

