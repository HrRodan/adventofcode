import math
import re

with open('input.txt') as file:
    times = [int(x) for x in re.findall(r'\d+', file.readline())]
    distances = [int(x) for x in re.findall(r'\d+', file.readline())]


# d = v_0*(t_ges-t_a)
# d = a*t_a*(t_ges-t_a) with a==1
# 0 = t_a^2-t_a*t_ges-d
# t_a = t_ges/2 +- sqrt(t_ges^2/4-d)
#
# def distance_traveled(t_total, t_accelerated):
#     return -t_accelerated**2+t_accelerated*t_total

def next_integer(z: float) -> int:
    return z + 1 if int(z) == z else math.ceil(z)


def prev_integer(z: float) -> int:
    return z - 1 if int(z) == z else math.floor(z)


def time_accelerated(t_total, distance):
    s = math.sqrt((t_total / 2) ** 2 - distance)
    return (t_total / 2 - s, t_total / 2 + s)


def times_to_win(t_total, distance):
    lower, upper = time_accelerated(t_total, distance)
    return prev_integer(upper) - next_integer(lower) + 1


result = math.prod(times_to_win(x, y) for x, y in zip(times, distances))
print(result)

# part 2
result = times_to_win(int(''.join(str(x) for x in times)), int(''.join(str(x) for x in distances)))
print(result)
