import curses
from board import Board
from util import ButtonMapEnum
from enum import Enum
from ai import AI

class Game:
    def __init__(self, stdscr):
        self.board = Board(4)
        self.board.spawn_tile()
        self.board.spawn_tile()
        self.over = False

        self.stdscr = stdscr
        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)
        self.clear_screen = True

        self.ai = AI()

    def draw_screen(self):
        self.stdscr.clear()
        self.stdscr.addstr(f"Score: {self.board.score}\n")
        self.stdscr.addstr("Use W/A/S/D to move. Press 'q' to quit.\n")
        self.stdscr.addstr(str(self.board) + "\n")

    def play(self):
        while not self.over:
            if self.clear_screen:
                self.draw_screen()
            
            move = self.stdscr.getch()

            if move == ord(ButtonMapEnum.QUIT.value):
                break

            if move == ord(ButtonMapEnum.HINT.value):
                best_move = self.ai.get_best_move(self.board)
                self.stdscr.addstr(f"AI suggests move: {best_move}\n")
                self.clear_screen = False
                self.stdscr.refresh()
                continue
            if move == ord(ButtonMapEnum.UP.value):
                self.board.shift_up()
                self.clear_screen = True
            elif move == ord(ButtonMapEnum.LEFT.value):
                self.board.shift_left()
                self.clear_screen = True
            elif move == ord(ButtonMapEnum.DOWN.value):
                self.board.shift_down()
                self.clear_screen = True
            elif move == ord(ButtonMapEnum.RIGHT.value):
                self.board.shift_right()
                self.clear_screen = True
            else:
                self.stdscr.addstr(f"Invalid move. Valid keys: {[button.value for button in ButtonMapEnum]}.\n")
                self.clear_screen = False
                self.stdscr.refresh()
                continue

            # only spawn a new tile if the board changed
            if self.board.board_changed:
                self.board.spawn_tile()

            if not self.board.can_move():
                self.over = True
                self.stdscr.addstr("Game Over!\n")

            if self.board.is_2048():
                self.over = True
                self.stdscr.addstr("You Win!\n")