import math
import re
from itertools import cycle

with open('input.txt') as file:
    steps_raw, map_raw = file.read().strip().split('\n\n')

steps = [0 if x == 'L' else 1 for x in steps_raw]
map_desert = {s: (l, r) for x in map_raw.split('\n') for s, l, r in [re.findall(r'[A-Z1-9]{3}', x)]}

# part 1
position = 'AAA'
for i, step in enumerate(cycle(steps)):
    if position == 'ZZZ':
        print(i)
        break
    position = map_desert[position][step]


# part 2
def get_count_until_z(position):
    for count, step in enumerate(cycle(steps)):
        if position[2] == 'Z':
            return count
        position = map_desert[position][step]


position_z_reached = [get_count_until_z(p) for p in map_desert if p[2] == 'A']
print(math.lcm(*position_z_reached))
