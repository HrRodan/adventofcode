import re
from itertools import islice
from typing import List
from heapq import merge
from utilities import batched

with open('input.txt') as file:
    almanac = file.read().split('\n\n')

seeds = [int(x) for x in re.findall(r'\d+', almanac[0])]

mappings = []
for mapping_raw in almanac[1:]:
    mapping = []
    for line in mapping_raw.split('\n')[1:]:
        mapping.append([int(x) for x in re.findall(r'\d+', line)])
    mappings.append(mapping)


def map_source_to_target(input_value: int, mapping: List[List[int]]):
    for t, s, r in mapping:
        if s <= input_value <= s + r - 1:
            return t + (input_value - s)
    return input_value


seed_locations = []
for s in seeds:
    current_position = s
    for m in mappings:
        current_position = map_source_to_target(current_position, m)
    seed_locations.append(current_position)

print(min(seed_locations))

#  %% part 2
mappings_as_range = [[[[x, x + r], [y, y + r]] for y, x, r in m] for m in mappings]


def non_overlapping(data):
    out = []
    starts = sorted([(i[0], 1) for i in data])  # start of interval adds a layer of overlap
    ends = sorted([(i[1], -1) for i in data])  # end removes one
    layers = 0
    current = []
    for value, event in merge(starts, ends):  # sorted by value, then ends (-1) before starts (1)
        layers += event
        if layers == 1:  # start of a new non-overlapping interval
            current.append(value)
        elif current:  # we either got out of an interval, or started an overlap
            current.append(value)
            out.append(current)
            current = []
    return out


def overlapping(x,y):
    overlap = [max(x[0], y[0]), min(x[-1], y[-1])]
    if overlap[1] > overlap[0]:
        return overlap
    else:
        return []

def non_overlap_from_first(range_seed, range_map):
    if not overlapping(range_seed, range_map):
        return [range_seed]
    non_overlaps = []
    if range_seed[0]<range_map[0]:
        non_overlaps.append([range_seed[0], range_map[0]])
    if range_seed[1]>range_map[1]:
        non_overlaps.append([range_map[1], range_seed[1]])
    return non_overlaps

# Ideas from Reddit
# Split each Seed Range along each intervall
# After each split minimum can be found at lowest range
# %%
seeds_range = [[x, x + y] for x, y in batched(seeds, 2)]

for mapping in mappings_as_range:
    overlap_ranges = []
    for s, t in mapping:
        new_seed_range = []
        for seed in seeds_range:
            overlap = overlapping(s, seed)
            if overlap:
                shift_left = overlap[0]-s[0]
                shift_right = overlap[1] - s[0]
                overlap_ranges.append([t[0] + shift_left, t[0] + shift_right])
            non_overlap = non_overlap_from_first(seed, s)
            for n in non_overlap:
                new_seed_range.append(n)
        seeds_range = new_seed_range
    seeds_range.extend(overlap_ranges)

print(min(x for x, _ in seeds_range))