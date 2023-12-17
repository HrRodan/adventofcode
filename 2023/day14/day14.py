import functools
from collections import defaultdict
from typing import List

with open('input.txt') as file:
    rocks_raw = [list(x.strip()) for x in file.readlines()]


@functools.cache
def total_load_of_line(rock_line: str):
    length_rock_line = len(rock_line)
    total_load = 0
    round_rock_value = length_rock_line
    new_rocks = ['.'] * length_rock_line
    current_location = 0
    for i, r in enumerate(rock_line, start=1):
        if r == '#':
            round_rock_value = length_rock_line - i
            new_rocks[i - 1] = '#'
            current_location = i
        elif r == 'O':
            new_rocks[current_location] = 'O'
            current_location += 1
            total_load += round_rock_value
            round_rock_value -= 1

    return new_rocks, total_load


transposed_rocks = list(zip(*rocks_raw))
result = sum(total_load_of_line(x)[1] for x in transposed_rocks)
print(result)


# part 2
def rotate_counter_clockwise(input_array: List[List]):
    return list(zip(*input_array))[::-1]


def get_new_array_and_total_load_hash(input_rocks):
    new_rocks_array = []
    total_load_array = []
    for r in input_rocks:
        rock_line, load_line = total_load_of_line(r)
        total_load_array.append(load_line)
        new_rocks_array.append(rock_line)

    return new_rocks_array, hash(tuple(total_load_array))


@functools.cache
def get_total_load_without_rolling(rock_line: str):
    length_rock_line = len(rock_line)
    return sum(
        length_rock_line - i for i, r in enumerate(rock_line) if r == 'O'
    )


def get_total_load_of_array_without_rolling(input_rocks):
    return sum(get_total_load_without_rolling(x) for x in input_rocks)


total_loads_seen = defaultdict(list)
total_load_after_cycle = {}

current_rocks = transposed_rocks
repetition_found = False
for i in range(1, 1000):
    for rotation_direction in range(4):
        # move all rocks to one side
        current_rocks, hash_value = get_new_array_and_total_load_hash(current_rocks)
        current_rocks = rotate_counter_clockwise(current_rocks)
        # check on east direction
        if rotation_direction == 3:
            # calculate load without rolling
            total_load = get_total_load_of_array_without_rolling(current_rocks)
            total_load_after_cycle[i] = total_load
            if hash_value in total_loads_seen:
                repetition_found = True
                start_of_repetition = total_loads_seen[hash_value][0]
                repetition_cycle = i - start_of_repetition
            total_loads_seen[hash_value].append(i)
    if repetition_found:
        break

result_part_2 = total_load_after_cycle[start_of_repetition + (1000000000 - start_of_repetition) % repetition_cycle]
print(result_part_2)
