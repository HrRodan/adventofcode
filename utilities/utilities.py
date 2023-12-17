import collections
import functools
from itertools import islice
from typing import Tuple, Optional

POINT_TYP = Tuple[int, int]


def sign(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


@functools.lru_cache(10000)
def tuple_add(t1: POINT_TYP, t2: POINT_TYP):
    return (t1[0] + t2[0], t1[1] + t2[1])


@functools.lru_cache(1000)
def tuple_add_nd(t1: Tuple[int, ...], t2: Tuple[int, ...]):
    return tuple(sum(x) for x in zip(t1, t2))


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


RANGE_TYP = Tuple[int, int]


def overlap(x: RANGE_TYP, y: RANGE_TYP) -> Optional[RANGE_TYP]:
    o = max(x[0], y[0]), min(x[-1], y[-1])
    return o if o[1] > o[0] else None


TURN_RIGHT = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}

TURN_LEFT = {v: k for k, v in TURN_RIGHT.items()}
