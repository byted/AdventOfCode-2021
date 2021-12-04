from io import BufferedRWPair
import re

with open('./input.txt') as f:
    # Sample input
    # 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    # 22 13 17 11  0
    # 8  2 23  4 24
    # 21  9 14 16  7
    # 6 10  3 18  5
    # 1 12 20 15 19
    lines = [l.strip() for l in f.readlines()]
    drawings = [int(n) for n in lines[0].split(',')]
    
    boards = []
    rows = []

    for line in lines[2:]:
        line = line.strip()
        if line == '':
            boards.append(rows)
            rows = []
        else:
            rows.append([int(n) for n in re.split(r'\s+', line)])
    boards.append(rows)

def mark_board(board, draw):
    for rx, row in enumerate(board):
        for cx, col in enumerate(row):
            if col == draw:
                board[rx][cx] = None

def check_board(board):  
    for row in board + list(zip(*board)):
        if all(c is None for c in row):
            return True
    
    return False

def calc_unmarked(board):
    return sum(sum(0 if c is None else c for c in row) for row in board)


def play_bingo(boards, drawings, try_to_lose=False):
    number_of_boards_to_solve = len(boards) if try_to_lose else 1 
    for draw in drawings:
        for bx, b in enumerate(boards):
            if b is None:
                continue

            mark_board(b, draw)
            if check_board(b):
                if boards.count(None) == number_of_boards_to_solve - 1:
                    return calc_unmarked(b) * draw
                boards[bx] = None

print(f'Part 1: {play_bingo(boards, drawings)}')
print(f'Part 2: {play_bingo(boards, drawings, try_to_lose=True)}')
