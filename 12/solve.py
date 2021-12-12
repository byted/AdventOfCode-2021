import re
import os
import sys
import math
from collections import defaultdict

graph = defaultdict(list)
for line in sys.stdin.readlines():
    f, t = line.strip().split('-')
    graph[f].append(t)
    if f != 'start':
        graph[t].append(f)

def paths_from_to(graph, start, end, use_special_visit_rule=False):
    found_paths = set()
    if not use_special_visit_rule:
        enumerate_paths(graph, found_paths, start, end)
        return found_paths

    for sp in [n for n in graph.keys() if n.islower() and n not in ['start', 'end']]:
        paths = set()
        enumerate_paths(graph, paths, start, end, special_node=sp)
        found_paths = found_paths.union(paths)
    return found_paths

def enumerate_paths(graph, found_paths, current, end, visited=defaultdict(lambda: 0), current_path=[], special_node=None):
    if current.islower():
        visited[current] += 1
    
    current_path.append(current)

    if current == end:
        found_paths.add(tuple(current_path))
    else:
        for next_node in graph[current]:
            if visited[next_node] == 0 or (special_node is not None and visited[next_node] == 1 and next_node == special_node):
                enumerate_paths(
                    graph, found_paths, next_node, end, visited=visited,
                    current_path=current_path, special_node=special_node
                )
    current_path.pop()
    if visited[current] > 0:
        visited[current] -= 1

print(f'Part 1: {len(paths_from_to(graph, "start", "end"))}')
print(f'Part 2: {len(paths_from_to(graph, "start", "end",  use_special_visit_rule=True))}')
