import curses
from board import Board

class Game:
    def __init__(self, stdscr):
        self.board = Board(4)
        self.board.spawn_tile()
        self.board.spawn_tile()
        self.over = False

        self.stdscr = stdscr
        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)

    def draw_screen(self):
        self.stdscr.clear()
        self.stdscr.addstr(f"Score: {self.board.score}\n")
        self.stdscr.addstr("Use W/A/S/D to move. Press 'q' to quit.\n")
        self.stdscr.addstr(str(self.board) + "\n")
        self.stdscr.refresh()

    def play(self):
        while not self.over:
            self.draw_screen()
            
            move = self.stdscr.getch()

            if move == ord("q"):
                break

            if move == ord("w"):
                self.board.shift_up()
            elif move == ord("a"):
                self.board.shift_left()
            elif move == ord("s"):
                self.board.shift_down()
            elif move == ord("d"):
                self.board.shift_right()
            else:
                self.stdscr.addstr("Invalid move. Please use w/a/s/d.\n")
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