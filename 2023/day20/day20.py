import math
from collections import defaultdict, deque
from typing import Dict

with open('input.txt') as file:
    modules_raw = [line.strip().split(' -> ') for line in file.readlines()]

flip_flop_modules: Dict[str, bool] = {}
conjunction_modules: Dict[str, Dict[str, bool]] = defaultdict(dict)
all_modules = set()
module_connections = defaultdict(list)

for src, tgts in modules_raw:
    tgts = [e.strip() for e in tgts.split(',')]
    module_typ = src[0]
    module_name = src[1:] if src != 'broadcaster' else 'broadcaster'
    all_modules.add(module_name)
    for tgt in tgts:
        module_connections[module_name].append(tgt)
        all_modules.add(tgt)
    if module_typ == '%':
        flip_flop_modules[src[1:]] = False
    elif module_typ == '&':
        conjunction_modules[module_name] = {}

for c in conjunction_modules:
    conjunction_modules[c] = {k: False for k, v in module_connections.items() if c in v}

all_lengths = {k: len(v) for k, v in module_connections.items()}

# for part 2 look at inputs to previous conjunction module
previous_to_rx = next(k for k, v in module_connections.items() if 'rx' in v)
inputs_to_previous = {x: [] for x in conjunction_modules[previous_to_rx]}

count_high_pulses = 0
count_low_pulses = 0
for i in range(1, 10000):
    # button press
    count_low_pulses += 1
    pulses_to_compute = deque([('broadcaster', False)])
    while pulses_to_compute:
        src, value = pulses_to_compute.popleft()
        targets = module_connections[src]
        if value:
            count_high_pulses += all_lengths[src]
        else:
            count_low_pulses += all_lengths[src]
        for t in targets:
            if t in flip_flop_modules:
                if value:
                    continue
                flip_flop_modules[t] = not flip_flop_modules[t]
                pulses_to_compute.append((t, flip_flop_modules[t]))
            elif t in conjunction_modules:
                if t == previous_to_rx and value:
                    inputs_to_previous[src].append(i)
                conjunction_modules[t][src] = value
                if value and all(conjunction_modules[t].values()):
                    pulses_to_compute.append((t, False))
                else:
                    pulses_to_compute.append((t, True))
    if i == 1000:
        print(count_high_pulses * count_low_pulses)

print(math.lcm(*[x[0] for x in inputs_to_previous.values()]))
