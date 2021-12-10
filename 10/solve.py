import re
import os
import sys
import math
from collections import defaultdict

bracket_mapping = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

part1_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137 
}

part2_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4 
}

def check_syntax(line):
    '''
    Analyzes a line. Returns (True, error_bracket) for corrupted and (False, remaining_stack) for incomplete.
    If no error is found, return (None, None)
    '''
    stack = []
    for bracket in line:
        if bracket in bracket_mapping:
            stack.append(bracket_mapping[bracket])
        else:
            if stack.pop() != bracket:
                return True, bracket
    
    if len(stack) > 0:
        return False, stack
    
    return (None, None)

def score_part1(syntax_analysis):
    return sum(part1_scores[wrong_bracket] for is_corrupted, wrong_bracket in syntax_analysis if is_corrupted)

def score_part2(syntax_analysis):
    def score_stack(s):
        score = 0
        for c in s:
            score = score * 5 + part2_scores[c]
        return score

    remaining_stacks = (remaining_stack for is_complete, remaining_stack in syntax_analysis if not is_complete)
    scores = sorted(score_stack(reversed(stack)) for stack in remaining_stacks)
    return scores[len(scores)//2]

syntax_analysis = [check_syntax(line.strip()) for line in sys.stdin.readlines()]
print(f'Part 1: {score_part1(syntax_analysis)}')
print(f'Part 2: {score_part2(syntax_analysis)}')
