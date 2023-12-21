import math
import operator
import re
from collections import defaultdict
from typing import List, Tuple

from utilities import RANGE_TYP, overlap, non_overlap_from_first

with open('input.txt') as file:
    workflows, ratings = file.read().split('\n\n')

workflows_raw_dict = {x: y[:-1].split(',') for line in workflows.split('\n') for x, y in [line.split('{')]}
ratings = [tuple(int(x) for x in re.findall(r'\d+', line)) for line in ratings.split('\n')]

letter_dict = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3
}

op_dict = {
    '<': operator.lt,
    '>': operator.gt
}

workflows = defaultdict(list)
for w, fcts in workflows_raw_dict.items():
    for fct in fcts:
        match = re.match(r'([a-z])(<|>)(\d+):([a-zA-Z]+)', fct)
        if match:
            g = match.groups()
            workflows[w].append((letter_dict[g[0]], op_dict[g[1]], int(g[2]), g[3]))
        else:
            workflows[w].append(fct)


def get_workflow_fct(fct_list: List):
    def workflow_fct(input_rating: Tuple[int]):
        for fct in fct_list:
            if type(fct) is str:
                return fct
            pos, op_fct, value, target = fct
            if op_fct(input_rating[pos], value):
                return target

    return workflow_fct


workflow_fct = {x: get_workflow_fct(y) for x, y in workflows.items()}

a_ratings = []
r_ratings = []

for r in ratings:
    current_workflow = 'in'
    while current_workflow not in ['A', 'R']:
        current_workflow = workflow_fct[current_workflow](r)
    if current_workflow == 'A':
        a_ratings.append(r)
    elif current_workflow == 'R':
        r_ratings.append(r)

result = sum(y for a in a_ratings for y in a)
print(result)

# part 2

workflows_part2 = {}
for w, cmds in workflows.items():
    new_cmds = []
    for cmd in cmds:
        if type(cmd) is str:
            new_cmds.append(cmd)
            continue
        if cmd[1] == operator.lt:
            range_cmd = (0, cmd[2])
        else:
            range_cmd = (cmd[2] + 1, 4001)
        new_cmds.append((cmd[0], range_cmd, cmd[3]))
    workflows_part2[w] = new_cmds

# tuple(x, m, a, s)
start_range = tuple((1, 4001) for _ in range(4))


def follow_workflow(input_ranges: Tuple[RANGE_TYP], target: str):
    count_valid = 0
    if target == 'R':
        return 0
    if target == 'A':
        return math.prod(x[1] - x[0] for x in input_ranges)
    for cmd_tuple in workflows_part2[target]:
        if type(cmd_tuple) is str:
            count_valid += follow_workflow(input_ranges, cmd_tuple)
            break
        position, range_cmd, target = cmd_tuple
        overlap_range = overlap(input_ranges[position], range_cmd)
        if overlap_range:
            non_overlap_range = non_overlap_from_first(input_ranges[position], range_cmd)[0]
            input_range_list_overlap = list(input_ranges)
            input_range_list_non_overlap = input_range_list_overlap.copy()
            input_range_list_overlap[position] = overlap_range
            input_range_list_non_overlap[position] = non_overlap_range
            # non overlap
            input_ranges = tuple(input_range_list_non_overlap)

            count_valid += follow_workflow(tuple(input_range_list_overlap), target)

    return count_valid

result = follow_workflow(start_range, 'in')
print(result)