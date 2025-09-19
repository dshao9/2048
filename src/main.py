from curses import wrapper
from game import Game

def run_game(stdscr):
    game = Game(stdscr)
    game.play()

if __name__ == "__main__":
    wrapper(run_game)