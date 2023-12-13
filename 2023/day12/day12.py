from collections import Counter
from itertools import permutations, islice, combinations
from sympy.utilities.iterables import multiset_permutations
import re

with open('input.txt') as file:
    springs_raw = [(x, tuple(int(y) for y in s.split(',')))
                   for line in file.readlines()
                   for x, s in [line.strip().split()]]


def replace_char_by_string(input_string, replace_string, replace_char='?'):
    replace_string_iter = iter(replace_string)
    return ''.join(next(replace_string_iter) if char == replace_char else char for char in input_string)


def spring_count_groups(spring_string):
    return tuple(len(x) for x in re.split(r'\.+', spring_string.strip('.')))


springs = []
count_arrangement = 0
for i, (s, c) in enumerate(springs_raw):
    total_springs = sum(c)
    letter_counter = Counter(s)
    open_positions = letter_counter['?']
    spring_count = letter_counter['#']
    open_springs = total_springs - spring_count
    open_empty = open_positions - open_springs
    all_open_permutations = list(multiset_permutations('#' * open_springs + '.' * open_empty))
    for co in all_open_permutations:
        test_string = replace_char_by_string(s, co)
        if spring_count_groups(test_string) == c:
            count_arrangement += 1

print(count_arrangement)