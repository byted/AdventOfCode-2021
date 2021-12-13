import re
import os
import sys
import math
from collections import defaultdict

dots = set()
folds = []
mode = 'dots'
for line in sys.stdin.readlines():
    if line == '\n':
        mode = 'folds'
        continue

    if mode == 'dots':
        dots.add(tuple([int(i) for i in line.strip().split(',')]))
    else:
        mirror_axis, mirror_pos = line.strip().split(' ')[2].split('=')
        folds.append((mirror_axis, int(mirror_pos)))



def mirror(mirror_axis, mirror_pos):
    return (mirror_pos-1) - (mirror_axis - (mirror_pos+1))

def fold(dots, fold):
    mirror_axis, mirror_pos = fold
    after_fold_dots = set()
    for x, y in dots:
        if mirror_axis == 'y' and y > mirror_pos:
            y = mirror(y, mirror_pos)
        elif mirror_axis == 'x' and x > mirror_pos:
            x = mirror(x, mirror_pos)
        after_fold_dots.add((x, y))

    return after_fold_dots

def print_sparse(dots):
    for r in range(max(y for _, y in dots)+1):
        for c in range(max(x for x, _ in dots)+1):
            print('#' if (c,r) in dots else ' ', end='')
        print('')


print(f'Part 1: {len(fold(dots, folds[0]))}')

for f in folds:
    dots = fold(dots, f)

print(f'Part 2:')
print_sparse(dots)
