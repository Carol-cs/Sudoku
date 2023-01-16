"""
Sudoku Generator
"""

import random
import copy

from solver import solve, is_valid

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
            if check_unique_sol(b, row, col):
                b[row][col] = 0
                num -= 1
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
    if level == "Easy":  # easy 35-41 blank
        level_num = random.randrange(35, 42)
    elif level == "Medium":  # medium 42-48 blank
        level_num = random.randrange(42, 49)
    elif level == "Hard":  # hard 49-55 blank
        level_num = random.randrange(49, 56)

    return clear_square(game_board, level_num)


def check_unique_sol(b, row, col):
    """
    check if the board has a unique solution after clearing the square value at position [row, col].
    :param b: board
    :param row: row of square
    :param col: column of square
    :return: IF the board has a unique solution:
                RETURN TRUE
             ELSE:
                FALSE
    """
    for i in range(1, 10):
        temp = copy.deepcopy(b)
        if temp[row][col] != i:
            temp[row][col] = 0
            if is_valid(b, i, [row, col]):
                temp[row][col] = i
                if solve(temp):
                    return False
    return True
