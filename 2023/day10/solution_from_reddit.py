import networkx as nx
import sys

data = sys.stdin.read().splitlines()
N, M = len(data), len(data[0])
G = nx.Graph()

for x, line in list(enumerate(data)):
    for y, char in list(enumerate(line)):
        # North neighbour
        if x > 0 and data[x-1][y] in "|7FS" and char in "|LJS":
            G.add_edge((x, y), (x-1, y))
        # East neighbour
        if y < M-1 and data[x][y+1] in "-J7S" and char in "-LFS":
            G.add_edge((x, y), (x, y+1))
        if char == "S":
            start = (x, y)

cycle = nx.find_cycle(G, start)
print("Part 1:", len(cycle)//2)

path_nodes = set(p[0] for p in cycle)
seen = set()

G2 = nx.grid_graph((N, M))
G2.remove_nodes_from(path_nodes)

for (x, y), (i, j) in cycle:
    # add nodes that are to the right side of a path
    dx, dy = i-x, j-y
    for i in (0, 1):
        node = x + i*dx - dy, y + i*dy + dx
        if node not in seen and node not in path_nodes:
            seen |= nx.node_connected_component(G2, node)

print("Part 2:", len(seen))

#Managed to make it fairly short using NetworkX. For Part 2, i took all the of points on the right side of
# my cycle path as staring points for floodfill. Do determine what are points on the "right" side, i took
# the differnce of two consecutive points (dx, dy) and took the points (x-dy, y+dx) and (x+dx-dy, y+dy+dx).
# This is like multiplying the difference vector with a rotation matrix.