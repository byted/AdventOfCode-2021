import re
import os
import sys
import math
from collections import defaultdict

# Some generic helpers... should go into a custom module at some point
def calc_neighbors(map, rx, cx):
    '''Returns a list of neighbors in the form of (value, row_index, column_index)'''
    neighbors = []
    if rx+1 < len(map):
        neighbors.append((map[rx+1][cx], rx+1, cx))
    if cx-1 >= 0:
        neighbors.append((map[rx][cx-1], rx, cx-1))
    if cx+1 < len(map[rx]):
        neighbors.append((map[rx][cx+1], rx, cx+1))
    if rx-1 >= 0:
        neighbors.append((map[rx-1][cx], rx-1, cx))
    
    if rx+1 < len(map) and cx+1 < len(map[rx]):
        neighbors.append((map[rx+1][cx+1], rx+1, cx+1))
    if rx+1 < len(map) and cx-1 >= 0:
        neighbors.append((map[rx+1][cx-1], rx+1, cx-1))
    if rx-1 >= 0 and cx+1 < len(map[rx]):
        neighbors.append((map[rx-1][cx+1], rx-1, cx+1))
    if rx-1  >= 0 and cx-1 >= 0:
        neighbors.append((map[rx-1][cx-1], rx-1, cx-1))
    
    return neighbors

def traverse_2d(map, func):
    for rx, r in enumerate(map):
        for cx, c in enumerate(r):
            func(map, rx, cx)
    
def print_2d(map):
    for r in map:
        print(r)


# Actual solution
map = [[int(c) for c in line.strip()] for line in sys.stdin.readlines()]

def execute_step(map):
    def flash_check(map, rx, cx, flashed):
        if map[rx][cx] > 9 and (rx, cx) not in flashed:
            flashed.add((rx, cx))
            for _, rx, cx in calc_neighbors(map, rx, cx):
                map[rx][cx] += 1
                flash_check(map, rx, cx, flashed)
        return flashed

    def apply_increase(map, rx, cx):
        map[rx][cx] += 1

    def apply_reset(map, rx, cx):
        if map[rx][cx] > 9:
            map[rx][cx] = 0    

    flashed = set()
    traverse_2d(map, apply_increase)
    traverse_2d(map, lambda m, rx, cx: flash_check(m, rx, cx, flashed))
    traverse_2d(map, apply_reset)
            
    
    return len(flashed)

def find_sync_flashing(map):
    i = 0
    while any(c != 0 for r in map for c in r):
        execute_step(map)
        i += 1
    return i

print(f'Part 1: {sum(execute_step(map) for _ in range(100))}')
print(f'Part 2: {find_sync_flashing(map)}')
