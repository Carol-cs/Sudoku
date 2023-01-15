"""
Sudoku Solver
"""

def print_board(b):
    """
    print board in good format in the console
    :param b: board
    """
    for i in range(len(b)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")

        for j in range(len(b[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j != 8:
                print(b[i][j], end=" ")
            else:
                print(b[i][j])


def find_empty(b):
    """
    find the next empty square on the board
    :param b: board
    :return: IF find an empty square:
                return position of the empty square in format [row, col]
            ELSE:
                return None
    """
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return [i, j]  # row, col

    return None


def is_valid(b, num, pos):
    """
    check if inserting num in pos is valid
    :param b: board
    :param num: number to be inserted on the board
    :param pos: position [row,col] of the square where the number needs to be inserted
    :return: IF valid:
                return True
            ELSE:
                return False
    """

    # check row
    for i in range(len(b[0])):
        if b[pos[0]][i] == num and i != pos[1]:
            return False

    # check column
    for i in range(len(b)):
        if b[i][pos[1]] == num and i != pos[0]:
            return False

    # check box
    box_row = pos[0] // 3  # get the position of box where the square (given pos) is located
    box_col = pos[1] // 3

    for i in range(box_row * 3, box_row * 3 + 3):
        for j in range(box_col * 3, box_col * 3 + 3):
            if b[i][j] == num and pos != [i, j]:
                return False

    return True


def solve(b):
    """
    solve the given sudoku board using backtracking
    Note: this function will modify the board
    :param b: board
    :return: IF the board is solvable:
                return True
            ELSE:
                return False
    """
    find = find_empty(b)
    if not find:  # base case: board is solved (no empty square is found)
        return True

    for i in range(1, 10):
        if is_valid(b, i, find):
            b[find[0]][find[1]] = i

            if solve(b):
                return True
            b[find[0]][find[1]] = 0  # reset to 0 if this approach cannot solve the board

    return False

