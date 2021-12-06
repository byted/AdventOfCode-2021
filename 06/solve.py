import re
import os
from collections import defaultdict

# fish_states = [int(i) for i in '3,4,3,1,2'.split(',')] # Sample data
fish_states = [int(i) for i in '1,3,3,4,5,1,1,1,1,1,1,2,1,4,1,1,1,5,2,2,4,3,1,1,2,5,4,2,2,3,1,2,3,2,1,1,4,4,2,4,4,1,2,4,3,3,3,1,1,3,4,5,2,5,1,2,5,1,1,1,3,2,3,3,1,4,1,1,4,1,4,1,1,1,1,5,4,2,1,2,2,5,5,1,1,1,1,2,1,1,1,1,3,2,3,1,4,3,1,1,3,1,1,1,1,3,3,4,5,1,1,5,4,4,4,4,2,5,1,1,2,5,1,3,4,4,1,4,1,5,5,2,4,5,1,1,3,1,3,1,4,1,3,1,2,2,1,5,1,5,1,3,1,3,1,4,1,4,5,1,4,5,1,1,5,2,2,4,5,1,3,2,4,2,1,1,1,2,1,2,1,3,4,4,2,2,4,2,1,4,1,3,1,3,5,3,1,1,2,2,1,5,2,1,1,1,1,1,5,4,3,5,3,3,1,5,5,4,4,2,1,1,1,2,5,3,3,2,1,1,1,5,5,3,1,4,4,2,4,2,1,1,1,5,1,2,4,1,3,4,4,2,1,4,2,1,3,4,3,3,2,3,1,5,3,1,1,5,1,2,2,4,4,1,2,3,1,2,1,1,2,1,1,1,2,3,5,5,1,2,3,1,3,5,4,2,1,3,3,4'.split(',')]

def run_step(fish_state):
    new_fish_state = defaultdict(lambda: 0)
    for days_left, num_of_fish in fish_state.items():
        if days_left == 0:
            new_fish_state[6] += num_of_fish
            new_fish_state[8] += num_of_fish
        else:
            new_fish_state[days_left-1] += num_of_fish
    return new_fish_state

def simulate(state, steps=80):
    fish_state = defaultdict(lambda: 0)
    for days_to_reproduce in state:
        fish_state[days_to_reproduce] += 1

    for i in range(steps):
        fish_state = run_step(fish_state)
    return sum(fish_state.values())

print(f'Part 1: {simulate(fish_states, steps=80)}')
print(f'Part 2: {simulate(fish_states, steps=256)}')
