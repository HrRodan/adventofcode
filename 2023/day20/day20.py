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

for c in conjunction_modules.keys():
    conjunction_modules[c] = {k: False for k, v in module_connections.items() if c in v}

other_modules = all_modules - module_connections.keys()

count_high_pulses = 0
count_low_pulses = 0
for i in range(1, 10000000):
    # button press
    rx_low_pulse = 0
    rx_high_pulse = 0
    count_low_pulses += 1
    pulses_to_compute = deque([('broadcaster', False)])
    while pulses_to_compute:
        src, value = pulses_to_compute.popleft()
        targets = module_connections[src]
        # if value:
        #     count_high_pulses += len(targets)
        # else:
        #     count_low_pulses += len(targets)
        for t in targets:
            if t == 'rx':
                if value:
                    count_high_pulses += 1
                else:
                    count_low_pulses += 1
            elif t in flip_flop_modules:
                if value:
                    continue
                flip_flop_modules[t] = not flip_flop_modules[t]
                pulses_to_compute.append((t, flip_flop_modules[t]))
            elif t in conjunction_modules:
                conjunction_modules[t][src] = value
                if all(conjunction_modules[t].values()):
                    pulses_to_compute.append((t, False))
                else:
                    pulses_to_compute.append((t, True))
    if rx_high_pulse != 0 or rx_low_pulse != 0:
        print(rx_low_pulse, rx_high_pulse)
    if rx_low_pulse == 1 and rx_high_pulse == 0:
        print(i)
        break

#print(count_high_pulses * count_low_pulses)
