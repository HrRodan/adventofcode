from collections import defaultdict
from itertools import product

import numpy as np
from scipy import ndimage

from utilities import tuple_add

with open('input.txt') as file:
    engine_raw = np.array([list(line.strip()) for line in file.readlines()])

engine_numbers = engine_raw.copy().astype(object)
engine_numbers[np.logical_not(np.char.isnumeric(engine_raw))] = -1
engine_numbers = engine_numbers.astype(np.byte)
engine_letters = np.logical_not(np.logical_or(np.char.isnumeric(engine_raw), engine_raw == '.'))

# %% find all start numbers
engine_numbers_bool = engine_numbers != -1
engine_numbers_bool = np.pad(engine_numbers_bool, pad_width=((0, 0), (0, 1)), mode='constant', constant_values=False)
all_starts = np.logical_and(engine_numbers_bool, np.logical_not(np.roll(engine_numbers_bool, 1, axis=1)))

# %% find all Fields with letter as neigbhor
fields_with_letter_as_neigbhor = ndimage.generic_filter(engine_letters, function=np.any, size=(3, 3), mode='constant',
                                                        cval=False)
fields_with_letter_as_neigbhor_set = {tuple(x) for x in np.transpose(np.nonzero(fields_with_letter_as_neigbhor))}

# %% find all fields with "*" as neighbor
fiels_with_star = engine_raw == '*'

# %% iterate through all starts
all_numbers_with_letter = []
all_points_with_values = {}
# unique identifier for numbers
count_numbers = 0
for point in np.transpose(np.nonzero(all_starts)):
    point = tuple(point)
    point_check = point
    letter_neigbhor = False
    number = ''
    number_points = []
    while engine_numbers_bool[point_check]:
        number += str(engine_numbers[point_check])
        if point_check in fields_with_letter_as_neigbhor_set:
            letter_neigbhor = True
        number_points.append(point_check)
        point_check = tuple_add(point_check, (0, 1))
    if letter_neigbhor:
        all_numbers_with_letter.append(int(number))
        for p in number_points:
            all_points_with_values[p] = count_numbers, int(number)
        count_numbers += 1

print(sum(all_numbers_with_letter))

# %% part 2
id_to_value = dict(all_points_with_values.values())

gear_number_neighbors = defaultdict(set)
# find neighboring ids for all stars
for g in np.transpose(np.nonzero(fiels_with_star)):
    g = tuple(g)
    for p in product((0,1,-1),repeat=2):
        p_new = tuple_add(g, p)
        if p_new in all_points_with_values:
            gear_number_neighbors[g].add(all_points_with_values[p_new][0])

gear_number_values = []
for x in gear_number_neighbors.values():
    if len(x) == 2:
        y = list(x)
        gear_number_values.append(id_to_value[y[0]] * id_to_value[y[1]])

print(sum(gear_number_values))
