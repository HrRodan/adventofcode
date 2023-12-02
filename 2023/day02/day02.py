import math
from typing import Dict, Tuple, List

import numpy as np

with open('input.txt') as file:
    input_raw = [line.strip() for line in file.readlines()]

# Order of tuple: (red, blue, green)

DRAW = Tuple[int, int, int]
GAME = List[DRAW]

games: Dict[int, GAME] = {}
for i, game_raw in enumerate(input_raw, start=1):
    game_raw = game_raw.split(': ')[1]
    draws_raw = game_raw.split('; ')
    draws = []
    for draw_raw in draws_raw:
        red, blue, green = 0, 0, 0
        colors_raw = draw_raw.split(', ')
        for color in colors_raw:
            color_int = int(color.split()[0])
            if 'red' in color:
                red = color_int
            elif 'blue' in color:
                blue = color_int
            elif 'green' in color:
                green = color_int
        draws.append((red, blue, green))
    games[i] = draws

ball_content = (12, 14, 13)


def game_is_valid(game: GAME, content: DRAW):
    max_per_color = (max(x) for x in zip(*game))
    return all(x >= y for x, y in zip(content, max_per_color))


valid_games_sum = sum(i for i, game in games.items() if game_is_valid(game, ball_content))
print(valid_games_sum)


# part2
def power_of_game(game: GAME):
    max_color = (max(x) for x in zip(*game))
    return math.prod(max_color)


games_power_sum = sum(power_of_game(game) for game in games.values())
print(games_power_sum)
