import re
import os
import sys
import math
from collections import defaultdict

map = [[int(c) for c in line.strip()] for line in sys.stdin.readlines()]

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
    
    return neighbors

def find_lowpoints(map):
    '''Returns a list of lowpoints in the form of (value, row_index, column_index)'''
    low_points = []
    for rx, r in enumerate(map):
        for cx, c in enumerate(r):
            if all(c < val for val, _, _ in calc_neighbors(map, rx, cx)):        
                low_points.append((c, rx, cx))
    return low_points

def calc_risk_level_for_map(map):
    return sum(p+1 for p,_,_ in find_lowpoints(map))

def calc_basins(map):
    '''Recursively calculate the basins for a given map. Returns a list of basin sizes'''

    def recurse(map, visited_points, basin_size, rx, cx):
        # There seem to be no "hills" in the basin, e.g. going in 0 -> 3 -> 2 -> 9)
        # or at least we do not care about the hills; all basins are delimited by a 9 
        neighbors = [(v, r, c) for v, r, c in calc_neighbors(map, rx, cx) if (r, c) not in visited_points and v != 9]
        visited_points.update([(rx, cx) for _, rx, cx in neighbors])
        
        basin_size += len(neighbors)
        for _, rx, cx in neighbors:
            # We're going depth-first so we use the basin_size of the finished sub-tree as input for the next one
            basin_size = recurse(map, visited_points, basin_size, rx, cx)
        return basin_size
    
    return [recurse(map, set([(rx, cx)]), 1, rx, cx) for v, rx, cx in find_lowpoints(map)]



print(f'Part 1: {calc_risk_level_for_map(map)}')
print(f'Part 2: {math.prod(sorted(calc_basins(map))[-3:])}')
