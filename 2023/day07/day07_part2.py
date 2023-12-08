from collections import Counter
from functools import total_ordering

with open('input.txt') as file:
    game = [
        (y[0], int(y[1]))
        for x in file.readlines()
        for y in [x.strip().split()]
    ]

# move J to last position
cards = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
card_value = {c: len(cards) - i for i, c in enumerate(cards)}


@total_ordering
class Hand():
    def __init__(self, hand_string: str):
        self.hand_string = hand_string
        self.hand_counter = Counter(hand_string)
        self.hand_type_value = self.get_hand_type_value(),
        self.hand_card_value = self.get_card_value()
        self.value = self.hand_type_value + self.hand_card_value

    def get_hand_type_value(self):
        j_count = self.hand_counter.get('J', 0)
        if j_count == 5:
            return 7
        self.hand_counter.pop('J', None)
        most_common_card_list = self.hand_counter.most_common(2)
        most_common = most_common_card_list[0][1]
        if most_common + j_count == 5:
            return 7
        if most_common + j_count == 4:
            return 6
        second_most_common = most_common_card_list[1][1]
        if most_common + j_count == 3:
            if second_most_common == 2:
                return 5
            else:
                return 4
        if most_common + j_count == 2:
            if second_most_common == 2:
                return 3
            else:
                return 2
        if most_common == 1:
            return 1

    def get_card_value(self):
        return tuple(card_value[x] for x in self.hand_string)

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        return f'Hand: {self.hand_string} - value {self.value}'


game_sorted = sorted([Hand(h), bid] for h, bid in game)
result = sum(bid * rank for rank, (_, bid) in enumerate(game_sorted, start=1))
print(result)
