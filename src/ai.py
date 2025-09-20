from board import Board
from util import ButtonMapEnum

class AI:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

    def get_best_move(self, board):

        moves = [
            (ButtonMapEnum.UP, self.score_board(board.shift_grid_up())),
            (ButtonMapEnum.DOWN, self.score_board(board.shift_grid_down())),
            (ButtonMapEnum.LEFT, self.score_board(board.shift_grid_left())),
            (ButtonMapEnum.RIGHT, self.score_board(board.shift_grid_right()))
        ]

        return max(moves, key=lambda x: x[1])[0]


    # simulate tables after shifting left, right, up and down
    # give each new board a hueristic score (NOT GAME SCORE) by scoring each row/column
    # sum the results of all 4 rows
    # sum the results of all 4 columns
    # sum the results of rows and columns to get the final score

    # Generate a score for the entire board by scoring each row and column
    def score_board(self, grid):
        total_score = 0
        # Score rows
        for row in grid:
            total_score += self.get_row_score(row)
        # Score columns
        for x in range(len(grid)):
            col = [grid[y][x] for y in range(len(grid))]
            total_score += self.get_row_score(col)
        return total_score

    def get_row_score(self, row):
        # score a row based on sum of squares, higher values = higher score
        sum_score = 0

        # count of empty tiles
        empty_count = 0

        # number of possible merges in this row if shifted left or right
        merge_potential = 0

        merge_counter = 0
        previous_tile = 0
        for i in range(len(row)):
            this_tile = row[i]

            sum_score += this_tile ** 2
            if this_tile == 0:
                empty_count += 1
            else:
                if this_tile == previous_tile:
                    merge_counter += 1
                elif merge_counter > 0:
                    merge_potential += 1 + merge_counter
                    merge_counter = 0

            previous_tile = this_tile

        if merge_counter > 0:
            merge_potential += 1 + merge_counter

        return sum_score + empty_count + merge_potential