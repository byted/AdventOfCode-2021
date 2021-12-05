import re
import os
from collections import defaultdict

with open(os.path.dirname(os.path.realpath(__file__)) + '/input.txt') as f:
    # Sample input
    # 0,9 -> 5,9
    # 8,0 -> 0,8
    # 9,4 -> 3,4
    # 2,2 -> 2,1
    # 7,0 -> 7,4
    # 6,4 -> 2,0
    # 0,9 -> 2,9
    # 3,4 -> 1,4
    # 0,0 -> 8,8
    # 5,5 -> 8,2
    vents = [[int(i) for i in re.match(r'^(\d+),(\d+) -> (\d+),(\d+)$', l).groups()] for l in f.readlines()]

def map_out_vents(vents, with_diagonals=True):
    vent_mapping = defaultdict(lambda: 0)

    for x1,y1,x2,y2 in vents:
        if not with_diagonals and x1 != x2 and y1 != y2:
            continue
        x_r = list(range(x1, x2+1)) if x2 > x1 else list(reversed(range(x2, x1+1)))
        y_r = list(range(y1, y2+1)) if y2 > y1 else list(reversed(range(y2, y1+1)))
        if len(x_r) == 1:
            x_r = x_r * len(y_r)
        
        if len(y_r) == 1:
            y_r = y_r * len(x_r)

        for x, y in zip(x_r, y_r):
            vent_mapping[f'{x}-{y}'] += 1
    return vent_mapping

def count_overlaps(vent_mapping):
    return len([v for v in vent_mapping.values() if v > 1])

print(f'Part 1: {count_overlaps(map_out_vents(vents, with_diagonals=False))}')
print(f'Part 2: {count_overlaps(map_out_vents(vents))}')
