import numpy as np

with open('input.txt') as file:
    value_history = [np.array([int(x) for x in line.strip().split()]) for line in file.readlines()]


def interpolate_value(array_in: np.array):
    last_values = [array_in[-1]]
    first_values = [array_in[0]]
    while not np.all(array_in == 0):
        array_in = np.diff(array_in)
        last_values.append(array_in[-1])
        first_values.append(array_in[0])
    fill_value_left = 0
    for v in first_values[-2::-1]:
        fill_value_left = v - fill_value_left
    return fill_value_left, sum(last_values)


interpolated_values = [interpolate_value(x) for x in value_history]
print(sum(x[1] for x in interpolated_values))
print(sum(x[0] for x in interpolated_values))
