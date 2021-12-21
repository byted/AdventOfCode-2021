import sys
import math
from functools import cache
# Sample Input
# Player 1 starting position: 4
# Player 2 starting position: 8
TRAINING_GAME_PLAYER1_START = 4
TRAINING_GAME_PLAYER2_START = 8

# Real Input
# Player 1 starting position: 4
# Player 2 starting position: 9
FULL_GAME_PLAYER1_START = 4
FULL_GAME_PLAYER2_START = 9

TRAINING_GAME_SCORE_THRESH = 1000
MULTIVERSE_GAME_SCORE_THRESH = 21

def roll(i, offset=0):
    # player 1: offset=0
    # player 2: offset=3
    return ((6*i+1+offset-1)%100+1) + ((6*i+2+offset-1)%100+1) + ((6*i+3+offset-1)%100+1)

def get_winner(p1_spot, p2_spot):
    def move_player_and_check_if_won(i, current_spot, current_score, offset=0):
        new_spot = (current_spot + roll(i, offset=offset) -1)%10+1 # -1/+1 to allow modulo "starting" at 1
        current_score += new_spot
        if current_score >= TRAINING_GAME_SCORE_THRESH:
            return True, None, None
        return False, new_spot, current_score

    def number_of_past_rolls(i):
        return 2*i*3 # both players rolled (*2) three times (*3) in each iteration

    p1_score = 0
    p2_score = 0
    i=0
    while True:
        has_won, p1_spot, p1_score = move_player_and_check_if_won(i, p1_spot, p1_score)
        if has_won:
            return p2_score * (number_of_past_rolls(i)+3)

        has_won, p2_spot, p2_score = move_player_and_check_if_won(i, p2_spot, p2_score, offset=3)
        if has_won:
            return p1_score * (number_of_past_rolls(i)+6)

        i+=1

# Let's do it bottom-up
# Assuming we're one throw from a player winning, we can calculate the outcomes for all dice rolls
# and save how often each player as won for each of the 27 rolls. Then, we can save it as
# p1_pos, p1_score, p2_pos, p2_score => (p1_wins, p2_wins)
# 
# We can then recursively descend and build up the storeage to easily look up already computed sub-trees

@cache
def dirac_rolls():
    # we always roll three times so sum up directly all possible combinations
    return [sum((i,j,k))+3 for i in range(3) for j in range(3) for k in range(3)]

def calc_next_spots(spots):
        return [(spots + roll - 1)%10+1 for roll in dirac_rolls()]

@cache
def multiverse(p1_spots, p1_score, p2_spots, p2_score, current_player='p1'):
    # base case: we're after the roll that pushed one player into the winning score
    if p1_score >= MULTIVERSE_GAME_SCORE_THRESH:
        return 1, 0
    if p2_score >= MULTIVERSE_GAME_SCORE_THRESH:
        return 0, 1
    
    # otherwise, roll again and recursively run for all possible dirac results
    if current_player == 'p1':
        subtree = [multiverse(next_spot, p1_score + next_spot, p2_spots, p2_score, current_player='p2') for next_spot in calc_next_spots(p1_spots)]
    else:
        subtree = [multiverse(p1_spots, p1_score, next_spot, p2_score + next_spot, current_player='p1') for next_spot in calc_next_spots(p2_spots)]
    return sum([i for i,_ in subtree]), sum([i for _,i in subtree])


print(f'Part 1: {get_winner(FULL_GAME_PLAYER1_START, FULL_GAME_PLAYER2_START)}')
print(f'Part 2: {max(multiverse(FULL_GAME_PLAYER1_START, 0, FULL_GAME_PLAYER2_START, 0, "p1"))}')

