"""
Sudoku Generator
"""

import random
import copy

from solver import solve

# generate a list containing 1-9
arr = []
for i in range(1, 10):
    arr.append(i)


def fill_diagonal(b):
    """
    randomly fill a diagonal of 3x3 boxes
    Note: this function will modify the board
    :param b: board
    """
    for i in range(3):
        random.shuffle(arr)
        p = 0
        for j in range(i * 3, i * 3 + 3):
            for k in range(i * 3, i * 3 + 3):
                b[j][k] = arr[p]
                p += 1


def fill_correct_diagonal(b):
    """
    try to solve the board having a randomly filled diagonal of 3x3 boxes to GENERATE a complete sudoku board
    Note: this function will modify the board
    :param b: board
    """
    fill_diagonal(b)
    while True:
        if solve(b):
            break
        else:
            fill_diagonal(b)
            continue


def clear_square(b, num):
    """
    clear some squares based on the given num to generate an unsolved board.
    Note: this function will modify the board
    :param b:board
    :param num:number of squares to be cleared
    :return:an unsolved board
    """
    while num > 0:
        row = random.randrange(0, 9)
        col = random.randrange(0, 9)
        if b[row][col] != 0:
            backup = copy.deepcopy(b)
            b[row][col] = 0
            if solve(b):  # make sure that the board remains solvable when a square is cleared.
                backup[row][col] = 0
                num -= 1
            b = copy.deepcopy(backup)
    return b


def generator(level):
    """
    generate an unsolved board based on the given level
    :param level: selected Sudoku game difficulty
    :return: an unsolved board that matches the required difficulty
    """

    game_board = [[0 for _ in range(9)] for _ in range(9)]  # create an empty board
    fill_correct_diagonal(game_board)  # create a randomly generated and completed board
    level_num = 0
    if level == "Easy":  # easy 40-46 blank
        level_num = random.randrange(40, 47)
    elif level == "Medium":  # medium 47-53 blank
        level_num = random.randrange(47, 54)
    elif level == "Hard":  # hard 54-60 blank
        level_num = random.randrange(54, 61)

    return clear_square(game_board, level_num)
