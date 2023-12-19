import operator
import re
from collections import defaultdict
from typing import List, Tuple

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
