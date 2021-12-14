import re
import os
import sys
import math
from collections import defaultdict
from collections import Counter


mode = 'template'
rules = defaultdict(lambda: defaultdict(lambda: None))
template = None
for line in sys.stdin.readlines():
    if line == '\n':
        mode = 'rules'
        continue
    if mode == 'template':
        template = line.strip()
    else:
        source, target = line.strip().split(' -> ')
        rules[source[0]][source[1]] = target

def apply_template(pairs, rules):
    new_pairs = defaultdict(int)
    for pair, cnt in pairs.items():
        target = rules[pair[0]][pair[1]]
        if target is None:
            new_pairs[(pair[0], pair[1])] = cnt
        else:
            new_pairs[(pair[0], target)] += cnt
            new_pairs[(target, pair[1])] += cnt
    return new_pairs

def execute(template, rules, n):
    pairs = defaultdict(int)
    for p in zip('-'+template, template+'-'):
        pairs[p] += 1

    for _ in range(n):
        pairs = apply_template(pairs, rules)
    return pairs

def calc_score(pairs):
    counts = defaultdict(int)
    for pair, cnt in pairs.items():
        for c in pair:
            if c != '-':
                counts[c] += cnt

    high = 0
    low = sys.maxsize
    for i, n in counts.items():
        if n > high:
            high = n
        if n < low:
            low = n
    
    return high//2 - low//2

print(f'Part 1: {calc_score(execute(template, rules, 10))}')
print(f'Part 2: {calc_score(execute(template, rules, 40))}')