import pygame

import copy
import time
from solver import solve, is_valid
from generator import generator

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 740
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (82, 164, 255)
GREY = (128, 128, 128)
PURPLE = (151, 78, 252)
RED = (250, 85, 85)
PINK = (242, 206, 206)
GREEN = (66, 219, 107)
YELLOW = (240, 212, 24)


class Game:
    """
    Class used to initialize and create a window
    """
    window = None

    # initialize game record at the start of each game (when a new game window is opened)
    record = {'Easy': "N/A", 'Medium': "N/A", 'Hard': "N/A"}
    icon_img = pygame.image.load("imgs/sudoku.png")

    def __init__(self):
        pass

    def create_game(self):
        pygame.display.init()
        Game.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Sudoku")
        pygame.display.set_icon(Game.icon_img)


class Menu:
    """
    Class used to create a menu
    """


    def __init__(self):
        self.button_easy = MenuButtons("Easy", 25, BLACK, BLACK, 3, 260)
        self.button_medium = MenuButtons("Medium", 22, BLACK, BLACK, 3, 360)
        self.button_hard = MenuButtons("Hard", 25, BLACK, BLACK, 3, 460)
        self.button_exit = MenuButtons("Exit", 25, BLACK, BLACK, 3, 560)
        self.button_easy_hover = MenuButtons("Easy", 30, WHITE, BLUE, 0, 260)
        self.button_medium_hover = MenuButtons("Medium", 27, WHITE, BLUE, 0, 360)
        self.button_hard_hover = MenuButtons("Hard", 27, WHITE, BLUE, 0, 460)
        self.button_exit_hover = MenuButtons("Exit", 30, WHITE, BLUE, 0, 560)

    def create_menu(self):
        pygame.display.init()
        pygame.display.set_caption("Sudoku")

        while True:
            Game.window.fill(WHITE)
            icon_img_width = Game.icon_img.get_width()
            Game.window.blit(Game.icon_img, (SCREEN_WIDTH / 2 - icon_img_width / 2, 120))

            self.check_button_hover()
            self.get_event()

            pygame.display.update()  # Make the window updated

    def get_event(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_easy.detect_mouse_hover():
                    MainGame("Easy").start_game()
                elif self.button_medium.detect_mouse_hover():
                    MainGame("Medium").start_game()
                elif self.button_hard.detect_mouse_hover():
                    MainGame("Hard").start_game()
                elif self.button_exit.detect_mouse_hover():
                    exit()

    def check_button_hover(self):
        """Check if the mouse is hovering over the button"""
        if self.button_easy.detect_mouse_hover():
            self.button_easy_hover.button_text()
        else:
            self.button_easy.button_text()
        if self.button_medium.detect_mouse_hover():
            self.button_medium_hover.button_text()
        else:
            self.button_medium.button_text()
        if self.button_hard.detect_mouse_hover():
            self.button_hard_hover.button_text()
        else:
            self.button_hard.button_text()
        if self.button_exit.detect_mouse_hover():
            self.button_exit_hover.button_text()
        else:
            self.button_exit.button_text()


class MenuButtons:
    """Class used to create and decorate buttons on menus"""

    def __init__(self, text, font_size, text_color, button_color, side_width, pos_y):
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.button_color = button_color
        self.side_width = side_width
        self.pos_y = pos_y

    def create_button(self):
        return pygame.draw.rect(Game.window, self.button_color,
                                pygame.Rect(SCREEN_WIDTH / 2 - 100, self.pos_y, 200, 50),
                                self.side_width, 15)

    def create_text(self):
        """Used to create text part of buttons"""
        pygame.font.init()
        font = pygame.font.Font('fonts/ghostclan.ttf', self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, self.pos_y + 25))
        Game.window.blit(text_surface, text_rect)

    def button_text(self):
        """combine create_button and create_text"""
        self.create_button()
        self.create_text()

    def detect_mouse_hover(self):
        """check if the mouse is hovering over a button"""
        return self.create_button().collidepoint(pygame.mouse.get_pos())


class MainGame:
    """
    Class used to create a new sudoku game based on selected difficulty
    """
    key = None

    def __init__(self, level):
        self.level = level
        if level == "Easy":
            pygame.display.set_caption("Sudoku-Easy")
        elif level == "Medium":
            pygame.display.set_caption("Sudoku-Medium")
        elif level == "Hard":
            pygame.display.set_caption("Sudoku-Hard")
        self.record = Game.record.get(self.level)

        self.game_board_gui = GameBoard(generator(self.level), SCREEN_WIDTH)
        self.note_mode = False
        self.check_status = ""

        self.visualizing = False  # determine if the program is visualizing the solution

        self.start_time = time.time()

        self.timing = True  # the timer will start as soon as the game starts.
        # will be cleared when click "Visual" or "Answer"
        # will restart when click "Reset" or "New Board"

        self.click_answer = False  # used to disallow to check after "Answer" until clicking "New Board"
        self.current_time = 0

        # buttons
        self.button_erase = MainGameButtons("Erase", "verdana", 15, BLACK, [100, 30], BLUE, 2,
                                            [25, SCREEN_WIDTH + 65])
        self.button_note = None
        self.button_check = None
        self.button_reset = None
        self.button_new = MainGameButtons("New Board", "verdana", 15, BLACK, [100, 30], PURPLE, 2,
                                          [25 + 115, SCREEN_WIDTH + 155])
        self.button_visual = MainGameButtons("Visual", "verdana", 15, BLACK, [100, 30], PURPLE, 2,
                                             [25 + 115 * 2, SCREEN_WIDTH + 155])
        self.button_answer = MainGameButtons("Answer", "verdana", 15, BLACK, [100, 30], PURPLE, 2,
                                             [25 + 115 * 3, SCREEN_WIDTH + 155])
        self.button_return = MainGameButtons("RETURN", "verdana", 15, BLACK, [215, 30], BLACK, 2,
                                             [25, SCREEN_WIDTH + 200])
        self.button_exit = MainGameButtons("EXIT", "verdana", 15, BLACK, [215, 30], BLACK, 2,
                                           [25 + 115 * 2, SCREEN_WIDTH + 200])

    def start_game(self):

        while True:
            Game.window.fill(WHITE)
            self.get_event()
            self.display_top_text()
            self.game_board_gui.display()
            self.display_all_buttons_text()
            pygame.display.update()  # Make the window updated

    def get_event(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and not self.visualizing and not self.click_answer \
                    and self.check_status != "Correct":
                if event.key == pygame.K_1:
                    MainGame.key = 1
                if event.key == pygame.K_2:
                    MainGame.key = 2
                if event.key == pygame.K_3:
                    MainGame.key = 3
                if event.key == pygame.K_4:
                    MainGame.key = 4
                if event.key == pygame.K_5:
                    MainGame.key = 5
                if event.key == pygame.K_6:
                    MainGame.key = 6
                if event.key == pygame.K_7:
                    MainGame.key = 7
                if event.key == pygame.K_8:
                    MainGame.key = 8
                if event.key == pygame.K_9:
                    MainGame.key = 9
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.visualizing and not self.click_answer and self.check_status != "Correct":
                    pos = pygame.mouse.get_pos()
                    clicked_square = self.game_board_gui.pos_to_row_col(pos)
                    if clicked_square:
                        self.game_board_gui.select(clicked_square[0], clicked_square[1])
                        MainGame.key = None

                if self.button_erase.detect_mouse_hover():
                    if self.game_board_gui.selected:
                        MainGame.key = None
                        self.game_board_gui.place_number(0)
                        self.game_board_gui.clear_note()

                if self.button_note.detect_mouse_hover():
                    self.note_mode = not self.note_mode
                if self.button_check.detect_mouse_hover() and not self.visualizing and not self.click_answer:
                    self.check_status = self.game_board_gui.check()
                    if self.check_status == "Correct":
                        self.timing = False

                        if self.game_board_gui.selected:
                            # unselect Square
                            row = self.game_board_gui.selected[0]
                            col = self.game_board_gui.selected[1]
                            self.game_board_gui.squares[row][col].selected = False
                            self.game_board_gui.selected = None

                if self.button_reset.detect_mouse_hover() and not self.visualizing and not self.click_answer \
                        and self.check_status != "Correct":
                    self.game_board_gui = GameBoard(self.game_board_gui.original_board, SCREEN_WIDTH)
                    self.check_status = ""
                    self.timing = True
                    self.start_time = time.time()

                if self.button_new.detect_mouse_hover():
                    self.game_board_gui = GameBoard(generator(self.level), SCREEN_WIDTH)
                    self.check_status = ""
                    self.click_answer = False
                    self.visualizing = False
                    self.timing = True
                    self.start_time = time.time()

                if self.button_visual.detect_mouse_hover():
                    self.visualizing = True
                    self.timing = False
                    self.game_board_gui = GameBoard(self.game_board_gui.original_board, SCREEN_WIDTH)
                    self.check_status = ""
                    self.start_time = time.time()
                    self.visual_solve()

                if self.button_answer.detect_mouse_hover():
                    self.click_answer = True
                    self.game_board_gui.squares = self.game_board_gui.init_squares(self.game_board_gui.solved_board)
                    self.game_board_gui.selected = None
                    self.timing = False
                if self.button_return.detect_mouse_hover():
                    Menu().create_menu()
                    self.timing = False
                if self.button_exit.detect_mouse_hover():
                    self.timing = False
                    exit()

        # check if the user tries to place numbers or make notes on selected squares.
        if self.game_board_gui.selected and MainGame.key is not None:
            if self.note_mode:
                if self.game_board_gui.get_selected_square().have_note_on_num(MainGame.key):
                    self.game_board_gui.get_selected_square().set_note(MainGame.key, False)
                else:
                    self.game_board_gui.make_note(MainGame.key)
            else:
                self.game_board_gui.clear_note()
                self.game_board_gui.place_number(MainGame.key)
            MainGame.key = None

    def hms_to_s(self, hms):
        """
        convert time units from H:M:S to seconds
        :param hms: a string, time in H:M:S
        :return: an integer, seconds
        """
        split_hms = hms.split(":")
        return int(split_hms[0]) * 3600 + int(split_hms[1]) * 60 + int(split_hms[2])

    def display_all_buttons_text(self):
        """
        display all text on buttons and check status
        """
        self.button_erase.button_text()

        # change the background color of Note button based on the mode
        if self.note_mode:
            self.button_note = MainGameButtons("Note", "verdana", 15, WHITE, [100, 30], BLUE, 0,
                                               [25 + 115 * 3, SCREEN_WIDTH + 65])
        else:
            self.button_note = MainGameButtons("Note", "verdana", 15, BLACK, [100, 30], BLUE, 2,
                                               [25 + 115 * 3, SCREEN_WIDTH + 65])
        self.button_note.button_text()

        if self.visualizing or self.click_answer or self.check_status == "Correct":
            self.button_check = MainGameButtons("Check", "verdana", 15, WHITE, [100, 30], GREY, 0,
                                                [25, SCREEN_WIDTH + 110])
            self.button_reset = MainGameButtons("Reset", "verdana", 15, WHITE, [100, 30], GREY, 0,
                                                [25, SCREEN_WIDTH + 155])
        else:
            self.button_check = MainGameButtons("Check", "verdana", 15, BLACK, [100, 30], RED, 2,
                                                [25, SCREEN_WIDTH + 110])
            self.button_reset = MainGameButtons("Reset", "verdana", 15, BLACK, [100, 30], PURPLE, 2,
                                                [25, SCREEN_WIDTH + 155])
        self.button_check.button_text()
        self.button_reset.button_text()
        self.button_new.button_text()
        self.button_visual.button_text()
        self.button_answer.button_text()
        self.button_return.button_text()
        self.button_exit.button_text()

        if self.check_status == "Incomplete":
            self.add_text("Incomplete...", 'fonts/zorque.otf', 25, BLACK, [SCREEN_WIDTH / 2, SCREEN_WIDTH + 125])
        elif self.check_status == "Correct":
            self.add_text("CORRECT!", 'fonts/zorque.otf', 25, GREEN, [SCREEN_WIDTH / 2, SCREEN_WIDTH + 125])
        elif self.check_status == "Wrong":
            self.add_text("WRONG!", 'fonts/zorque.otf', 25, RED, [SCREEN_WIDTH / 2, SCREEN_WIDTH + 125])

    def display_top_text(self):
        """
        display text at the top of the board
        """
        # display level
        if self.level == "Easy":
            level_color = GREEN
        elif self.level == "Medium":
            level_color = YELLOW
        elif self.level == "Hard":
            level_color = RED
        self.add_text(self.level, 'verdana', 20, level_color, [40, 35])

        # display record
        if self.check_status == "Correct":
            # check if the current game hit a record
            if self.record == "N/A" or self.current_time < self.hms_to_s(self.record):
                formatted_current_time = self.format_time(self.current_time)
                record_rect = self.add_text(formatted_current_time, 'verdana', 20, BLACK,
                                            [SCREEN_WIDTH / 2, 35])
                self.record = formatted_current_time
                Game.record[self.level] = formatted_current_time
            else:
                record_rect = self.add_text(self.record, 'verdana', 20, BLACK,
                                            [SCREEN_WIDTH / 2, 35])
        else:
            record_rect = self.add_text(self.record, 'verdana', 20, BLACK, [SCREEN_WIDTH / 2, 35])

        medal_img = pygame.image.load("imgs/medal.png")
        medal_img_width = medal_img.get_width()
        Game.window.blit(medal_img, (SCREEN_WIDTH / 2 - record_rect.get_width() / 2 - medal_img_width, 22))

        # display timer
        if self.timing:
            self.current_time = int(time.time() - self.start_time)
            time_rect = self.add_text(self.format_time(self.current_time), 'verdana', 20, BLACK,
                                      [SCREEN_WIDTH - 50, 35])
        else:
            if self.check_status == "Correct":
                time_rect = self.add_text(self.format_time(self.current_time), 'verdana', 20, BLACK,
                                          [SCREEN_WIDTH - 50, 35])
            else:
                time_rect = self.add_text(self.format_time(0), 'verdana', 20, BLACK, [SCREEN_WIDTH - 50, 35])
        timer_img = pygame.image.load("imgs/timer.png")
        timer_img_width = timer_img.get_width()
        Game.window.blit(timer_img, (SCREEN_WIDTH - 50 - time_rect.get_width() / 2 - timer_img_width, 22))

    def add_text(self, text, font, font_size, text_color, pos):
        """
        create text based on text, font, font size, text color and position
        :return: generated text_surface
        """
        pygame.font.init()
        if "." in font:
            font = pygame.font.Font(font, font_size)
        else:
            font = pygame.font.SysFont(font, font_size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(pos[0], pos[1]))
        Game.window.blit(text_surface, text_rect)

        return text_surface

    def format_time(self, s):
        """
        convert time units from seconds to H:M:S
        :param s: seconds
        :return: a string, time in form H:M:S
        """
        second = s % 60
        minute = s // 60
        hour = minute // 60
        formatted_time = str(hour) + ":" + str(minute) + ":" + str(second)
        return formatted_time

    def visual_solve(self):
        """
        used to visualize the solution using backtracking algorithm
        :return: IF the board is solvable:
                    return True
                ELSE:
                    return False
        """
        find = self.find_empty_square()
        updated_board = self.game_board_gui.updated_board_array()
        if not find:  # base case: board is solved (no empty square is found)
            return True

        for i in range(1, 10):
            if self.visualizing:
                find.value = i
                find.visual_color = RED
                self.update_visual()

                time.sleep(0.05)

                if not is_valid(updated_board, i, [find.row, find.col]):
                    find.value = 0
                    continue

                find.visual_color = GREEN
                self.update_visual()

                if self.visual_solve():
                    return True

                find.value = 0  # reset to 0 if this approach cannot solve the board

        find.visual_color = BLACK
        self.update_visual()
        return False

    def find_empty_square(self):
        """
        find the next empty Square
        :return: IF find the next empty Square, return that Square, return None otherwise
        """
        for i in range(len(self.game_board_gui.squares)):
            for j in range(len(self.game_board_gui.squares[0])):
                if self.game_board_gui.squares[i][j].value == 0:
                    return self.game_board_gui.squares[i][j]

        return None

    def update_visual(self):
        """
        update the game interface when visualizing the solution
        """
        Game.window.fill(WHITE)
        self.get_event()
        self.display_top_text()
        self.display_all_buttons_text()
        self.game_board_gui.display()
        pygame.display.update()


class MainGameButtons:
    """
    Class used to create buttons for main game
    """

    def __init__(self, text, font, font_size, text_color, button_size, button_color, side_width, pos):
        self.text = text
        self.font = font
        self.font_size = font_size
        self.text_color = text_color
        self.button_size = button_size
        self.button_color = button_color
        self.side_width = side_width
        self.pos = pos

    def create_button(self):
        return pygame.draw.rect(Game.window, self.button_color,
                                pygame.Rect(self.pos[0], self.pos[1], self.button_size[0], self.button_size[1]),
                                self.side_width, 10)

    def create_text(self):
        """Used to create text part of buttons"""
        pygame.font.init()
        if "." in self.font:
            font = pygame.font.Font(self.font, self.font_size)
        else:
            font = pygame.font.SysFont(self.font, self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.pos[0] + self.button_size[0] / 2,
                                                  self.pos[1] + self.button_size[1] / 2))
        Game.window.blit(text_surface, text_rect)

    def button_text(self):
        """combine create_button and create_text"""
        self.create_button()
        self.create_text()

    def detect_mouse_hover(self):
        """check if the mouse is hovering over a button"""
        return self.create_button().collidepoint(pygame.mouse.get_pos())


class GameBoard:
    """
    Class used to create Sudoku board that contains 81 Square
    """

    def __init__(self, board, size):
        self.original_board = board
        self.solved_board = copy.deepcopy(board)
        solve(self.solved_board)
        self.size = size
        self.square_size = size / 9
        self.selected = None
        self.squares = self.init_squares(self.original_board)

    def init_squares(self, board):
        """
        initialize squares on Sudoku board, set pre_filled to true if the square is not zero
        :param board: sudoku game board
        :return: 2d array of Square
        """
        squares = [[Square(board[r][c], r, c, self.size) for c in range(len(board[0]))]
                   for r in range(len(board))]
        for r in range(len(squares)):
            for c in range(len(squares[0])):
                if self.original_board[r][c] != 0:
                    squares[r][c].pre_filled = True

        return squares

    def place_number(self, val):
        """
        place the number in square if that square is not pre_filled
        :param val: number placed on the square
        """
        if not self.get_selected_square().pre_filled:
            self.get_selected_square().set_value(val)

    def make_note(self, val):
        """
        add note in square if that square is not pre_filled
        :param val: number placed on the square in note mode
        """
        if not self.get_selected_square().pre_filled:
            self.get_selected_square().set_note(val, True)
            self.get_selected_square().value = 0

    def clear_note(self):
        """
        clear note in square if that square is not pre_filled
        """
        row = self.selected[0]
        col = self.selected[1]
        if not self.squares[row][col].pre_filled:
            self.squares[row][col].clear_note()

    def get_selected_square(self):
        """
        get the selected Square
        :return: selected Square
        """
        row = self.selected[0]
        col = self.selected[1]
        return self.squares[row][col]

    def display(self):
        """display the entire game board"""

        # show sides
        pygame.draw.rect(Game.window, BLACK, pygame.Rect(0, 50, self.size, self.size), 3)

        # show squares:
        for r in range(len(self.squares)):
            for c in range(len(self.squares[0])):
                self.squares[r][c].display()

        # show the lines between
        for i in range(len(self.squares)):
            if i % 3 == 0 and i != 0:
                thick = 3
            else:
                thick = 1

            pygame.draw.line(Game.window, BLACK, (0, 49 + i * self.square_size), (self.size, 49 + i * self.square_size),
                             thick)
            pygame.draw.line(Game.window, BLACK, (i * self.square_size, 49), (i * self.square_size, 49 + self.size),
                             thick)

    def select(self, row, col):
        """
        set all squares to be unselected and set the square at [row, col] to be selected.
        :param row: row of a specific Square
        :param col: column of a specific Square
        """

        # set all squares to be unselected
        for i in range(len(self.squares)):
            for j in range(len(self.squares[0])):
                self.squares[i][j].selected = False

        # set the specified square to be selected
        self.squares[row][col].selected = True
        self.selected = [row, col]

    def pos_to_row_col(self, pos):
        """
        convert the mouse position to the position of a Square on the game board in the form [row, col]
        :param pos: mouse position
        :return: IF the given mouse position matches a Square
                    return [row, col]
                ELSE:
                    return None
        """
        if pos[0] < self.size and 50 < pos[1] < self.size + 50:
            row = int((pos[1] - 50) // self.square_size)
            col = int(pos[0] // self.square_size)
            return [row, col]
        else:
            return None

    def check(self):
        """
        check if the board is completed, or if the completed board is solved correctly
        :return: IF the board is incomplete
                    return "Incomplete"
                IF the completed board is correct
                    return "Correct"
                IF the completed board is wrong
                    return "Wrong"
        """
        incorrect_squares = []
        for i in range(len(self.squares)):
            for j in range(len(self.squares[0])):
                if self.squares[i][j].value == 0:
                    return "Incomplete"
        for i in range(len(self.squares)):
            for j in range(len(self.squares[0])):
                if self.squares[i][j].value == self.solved_board[i][j]:
                    continue
                else:
                    incorrect_squares.append(self.squares[i][j])

        self.color_square(incorrect_squares)
        if len(incorrect_squares) == 0:
            return "Correct"
        else:
            return "Wrong"

    def color_square(self, incorrect_squares):
        """
        update Square color, mark invalid Squares
        :param incorrect_squares: an array of invalid squares
        """
        for i in range(len(self.squares)):
            for j in range(len(self.squares[0])):
                if not self.squares[i][j].pre_filled:
                    if self.squares[i][j] in incorrect_squares:
                        self.squares[i][j].wrong = True
                    else:
                        self.squares[i][j].wrong = False

    def updated_board_array(self):
        """
        used to create a 2d array based on the values on Square.
        :return: a 2d array whose elements are integer values  (0-9)
        """
        updated_board = []
        for r in range(len(self.squares)):
            lines = []
            for c in range(len(self.squares[0])):
                lines.append(self.squares[r][c].value)
            updated_board.append(lines)

        return updated_board


class Square:
    """
    Class used to create Square
    """

    def __init__(self, value, row, col, size):
        self.value = value

        # indicate if a specific number needs to be displayed as a note
        self.note = [[False for _ in range(3)] for _ in range(3)]

        self.row = row
        self.col = col
        self.size = size
        self.selected = False
        self.pre_filled = False
        self.wrong = False
        self.visual_color = None

    def display(self):
        """
        display each Square
        """
        pygame.font.init()
        square_size = self.size / 9
        sub_square_size = square_size / 3

        pos_x = self.col * square_size
        pos_y = self.row * square_size + 50

        display_note = self.display_note()

        # if the number on the square is invalid, it is marked red after the check
        if self.wrong:
            pygame.draw.rect(Game.window, PINK, (pos_x, pos_y, square_size + 1, square_size + 1), 0)

        # set color when visualizing
        if self.visual_color:
            if self.visual_color == BLACK:
                pygame.draw.rect(Game.window, self.visual_color, (pos_x, pos_y, square_size + 1, square_size + 1), 1)
            else:
                pygame.draw.rect(Game.window, self.visual_color, (pos_x, pos_y, square_size + 1, square_size + 1), 4)

        # display number or note on square
        if display_note and self.value == 0:
            font = pygame.font.SysFont("verdana", 12)
            for r in range(len(self.note)):
                for c in range(len(self.note[0])):
                    if self.note[r][c]:
                        first_num = r * 3 + 1
                        num = c + first_num
                        text_surface = font.render(str(num), True, GREY)

                        text_rect = text_surface.get_rect(center=(pos_x + sub_square_size * c + sub_square_size / 2,
                                                                  pos_y + sub_square_size * r + sub_square_size / 2))
                        Game.window.blit(text_surface, text_rect)
        elif not display_note and self.value != 0:
            font = pygame.font.SysFont("verdana", 35)
            if self.pre_filled:
                color = BLACK
            else:
                color = BLUE
            text_surface = font.render(str(self.value), True, color)
            text_rect = text_surface.get_rect(center=(pos_x + square_size / 2, pos_y + square_size / 2))
            Game.window.blit(text_surface, text_rect)

        # if the square is selected, add a blue frame
        if self.selected:
            pygame.draw.rect(Game.window, BLUE, (pos_x, pos_y, square_size + 1, square_size + 1), 4)

    def display_note(self):
        """
        check if at least one note is made
        :return: IF at least one note is made:
                    return True
                ELSE:
                    return False
        """
        for i in range(len(self.note)):
            for j in range(len(self.note[0])):
                if self.note[i][j]:
                    return True
        return False

    def have_note_on_num(self, val):
        """
        check if note already has a certain number.
        (If have, in note mode,  pressing the number will delete that number)
        :param val: number needs to be checked
        :return: True if note has val, False otherwise
        """
        row = (val - 1) // 3
        col = (val - 1) % 3
        return self.note[row][col]

    def set_value(self, val):
        """
        set value for Square
        :param val: value given to Square
        """
        self.value = val

    def set_note(self, val, has_value):
        """
        setup note
        :param val: number to be added/removed to/from note
        :param has_value: True if needs to add the val to note
                          False if need to remove the val from note
        """
        row = (val - 1) // 3
        col = (val - 1) % 3

        self.note[row][col] = has_value

    def clear_note(self):
        """
        clear all notes
        """
        self.note = [[False for _ in range(3)] for _ in range(3)]


if __name__ == "__main__":
    Game().create_game()
    Menu().create_menu()
