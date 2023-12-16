from typing import List

import numpy as np

with open('input.txt') as file:
    maps: List[np.ndarray] = [np.array([list(x) for x in line.strip().split('\n')]) == '#' for line in
                              file.read().split('\n\n')]


def find_mirror_lines(m: np.ndarray):
    shape = m.shape
    # horizontal mirror
    for ax in [0, 1]:
        for row in range(shape[ax] - 1):
            if np.array_equal(m.take(indices=row, axis=ax), m.take(indices=row + 1, axis=ax)):
                distance_to_end = shape[ax] - row - 1
                distance_to_start = row + 1
                m_truncated = m.take(
                    indices=range(max(0, row - distance_to_end + 1), min(shape[ax], row + distance_to_start + 1)),
                    axis=ax)
                if np.array_equal(m_truncated, np.flip(m_truncated, axis=ax)):
                    return ax, row + 1
    raise ValueError("No mirror line found")


result = [find_mirror_lines(m) for m in maps]
result_value = sum(x if ax == 1 else x * 100 for ax, x in result)
print(result_value)


def find_smudge_mirror(m: np.ndarray):
    shape = m.shape
    # horizontal mirror
    for ax in [0, 1]:
        for row in range(0, shape[ax] - 1):
            distance_to_end = shape[ax] - row - 1
            distance_to_start = row + 1
            m_truncated = m.take(
                indices=range(max(0, row - distance_to_end + 1), min(shape[ax], row + distance_to_start + 1)), axis=ax)
            not_equal = np.not_equal(m_truncated, np.flip(m_truncated, axis=ax))
            if np.sum(not_equal) == 2:
                return ax, row + 1
    raise ValueError("No smudge found")


result_part2 = [find_smudge_mirror(m) for m in maps]
result_value_part2 = sum(x if ax == 1 else x * 100 for ax, x in result_part2)
print(result_value_part2)
