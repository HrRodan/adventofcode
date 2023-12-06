import re
from collections import Counter

with open('input.txt') as file:
    cards = [
        [{int(z) for z in re.findall(r'\d+', x)} for x in y.split(':')[1].split('|')]
        for y in file.readlines()
    ]

number_cards = len(cards)

winning_cards = [x.intersection(y) for x, y in cards]
winning_cards_sum = sum(2 ** (len(x) - 1) for x in winning_cards if x)
print(winning_cards_sum)

# %%part2
winning_cards_range = {i: tuple(range(i + 1, min(i + len(x) + 1, number_cards + 1))) for i, x in
                       enumerate(winning_cards, start=1)}

cards_count = Counter({i: 1 for i in range(1, len(cards) + 1)})

for i in range(1, len(cards) + 1):
    cards_to_add = {x: cards_count[i] for x in winning_cards_range[i]}
    cards_count.update(cards_to_add)

print(cards_count.total())
