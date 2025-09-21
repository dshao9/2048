from board import Board
from util import ButtonMapEnum
from ai import AI
import time

class Game:
    def __init__(self, stdscr):
        self.board = Board(4)
        self.board.spawn_tile()
        self.board.spawn_tile()
        self.over = False

        self.stdscr = stdscr
        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)
        self.stdscr.scrollok(True)
        self.clear_screen = True

        self.ai = AI(stdscr=stdscr)

        self.auto_play = False

    def draw_screen(self):
        self.stdscr.clear()
        self.stdscr.addstr(f"Score: {self.board.score}\n")
        self.stdscr.addstr("Use W/A/S/D to move.\n")
        self.stdscr.addstr("Press 'q' to quit.\n")
        self.stdscr.addstr("Press 'h' for AI hint.\n")
        self.stdscr.addstr("Press 'g' for Autoplay.\n")
        self.stdscr.addstr(str(self.board) + "\n")

    def play(self):
        while not self.over:
            if self.clear_screen:
                self.draw_screen()

            if not self.board.can_move():
                self.over = True
                self.stdscr.nodelay(False)
                # self.stdscr.addstr(str(self.board) + "\n")
                self.stdscr.addstr("No moves left! Game Over!\n")
                self.stdscr.refresh()
                break

            if self.board.is_2048():
                self.over = True
                self.stdscr.addstr("You Win!\n")
                self.stdscr.refresh()
                break
            
            if self.auto_play:
                best_move = self.ai.get_best_move(self.board)
                if best_move is None:
                    self.over = True
                    self.stdscr.nodelay(False)
                    self.stdscr.addstr("AI couldn't find a move! Silly robot.\n")
                    self.stdscr.refresh()
                key = ButtonMapEnum[best_move].value
                self.stdscr.addstr(f"AI next move: {best_move}\n")
                self.stdscr.refresh()
                
                self.stdscr.nodelay(True)
                move = ord(key)
                input = self.stdscr.getch()
            else:
                input = self.stdscr.getch()
                move = input

            if input == ord(ButtonMapEnum.QUIT.value):
                break

            if input == ord(ButtonMapEnum.HINT.value):
                self.stdscr.addstr(f"Thinking...\n")
                self.stdscr.refresh()
                best_move = self.ai.get_best_move(self.board)
                self.stdscr.addstr(f"AI suggests move: {best_move}\n")
                self.clear_screen = False
                self.stdscr.refresh()
                continue

            if input == ord(ButtonMapEnum.AUTOPLAY.value):
                self.auto_play = not self.auto_play
                if not self.auto_play:
                    self.stdscr.nodelay(False)
                status = "enabled" if self.auto_play else "disabled"
                self.stdscr.addstr(f"Autoplay {status}.\n")
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

        self.stdscr.addstr("Press any key to exit...\n")
        self.stdscr.refresh()
        self.stdscr.getch()