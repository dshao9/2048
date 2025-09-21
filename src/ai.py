from board import ButtonMapEnum


# Borrowed from Robert Xiao's excellent blog post on 2048 AI
# http://robert-xiao.com/2014/04/14/2048-ai
# https://github.com/nneonneo/2048-ai
BASE_SCORE = 200000
MONO_WEIGHT = 47
EMPTY_WEIGHT = 270
MERGE_WEIGHT = 700
MONO_SCALE = 4
SUM_SCALE = 3.5
SUM_WEIGHT = 11


class AI:
    """ General AI strategy here is to simulate tables after shifting in every direction,
        give each new board a hueristic score (not game score) by scoring each row/column,
        sum the results of rows and columns to get the direction that yields the best
        total score (expectimax).

        Then generate all possible spawns of 2 and 4 on the new board and evaluate those boards
        recursively up to a certain depth
    """
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

        self.move_funcs = {
            ButtonMapEnum.UP.value: self.shift_grid_up_int64,
            ButtonMapEnum.DOWN.value: self.shift_grid_down_int64,
            ButtonMapEnum.LEFT.value: self.shift_grid_left_int64,
            ButtonMapEnum.RIGHT.value: self.shift_grid_right_int64
        }

        self.row_cache = {}
        self.board_cache = {}

        # precompute row scores since there are only 65536 possible rows
        self.init_rows()

    def get_best_move(self, board):
        """ Use expectimax to find the best move returns the corresponding ButtonMapEnum value """
        grid_int = self.grid_to_int64(board.grid)
        curr_depth = 0

        best_score = -1
        best_move = None

        for move, func in self.move_funcs.items():
            new_grid_int = func(grid_int)
            if new_grid_int != grid_int:
                score = self.evaluate_spawns(new_grid_int, curr_depth)
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move
    
    def evaluate_spawns(self, grid_int, depth):
        """ Evaluate all possible spawns of 2 and 4 on the current board 
            since we know the spawn probabilities. 
        """
        if depth >= self.max_depth:
            return self.score_board(grid_int)
        
        # retrieve board from cache if available
        if grid_int in self.board_cache:
            return self.board_cache[grid_int]

        score = 0
        empty_tiles = []
        for i in range(16):
            if ((grid_int >> (4 * i)) & 0xF) == 0:
                empty_tiles.append(i)

        if not empty_tiles:
            return self.score_board(grid_int)

        for tile in empty_tiles:
            new_grid_int_2 = grid_int | (1 << (4 * tile))
            score_2 = self.evaluate_board(new_grid_int_2, depth)
            score += score_2 * 0.9

            new_grid_int_4 = grid_int | (2 << (4 * tile))
            score_4 = self.evaluate_board(new_grid_int_4, depth)
            score += score_4 * 0.1

        res = score / len(empty_tiles)

        # cache board results
        self.board_cache[grid_int] = res
        return res

    def evaluate_board(self, grid_int, depth):
        """ Evaluate all moves on the current board """
        max_score = 0
        for move_func in self.move_funcs.values():
            new_grid_int = move_func(grid_int)
            if new_grid_int != grid_int:
                score = self.evaluate_spawns(new_grid_int, depth + 1)
                max_score = max(max_score, score)
        return max_score

    def grid_to_int64(self, grid):
        result = 0
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                value = grid[y][x]
                power = 0 if value == 0 else value.bit_length() - 1
                result |= (power & 0xF) << (4 * (y * len(grid) + x))
        return result
    
    def int64_to_grid(self, int64):
        grid = []
        for y in range(4):
            row = []
            for x in range(4):
                power = (int64 >> (4 * (y * 4 + x))) & 0xF
                value = 0 if power == 0 else 1 << power
                row.append(value)
            grid.append(row)
        return grid

    # shifting left = shift each row left
    def shift_grid_left_int64(self, grid_int64):
        new_grid_int64 = 0
        for y in range(4):
            row = (grid_int64 >> (16 * y)) & 0xFFFF
            new_row = self.shift_row_int16_left(row)
            new_grid_int64 |= (new_row & 0xFFFF) << (16 * y)
        return new_grid_int64
    
    # shifting right = reverse each row, shift left, reverse again
    def shift_grid_right_int64(self, grid_int64):
        new_grid_int64 = 0
        for y in range(4):
            row = (grid_int64 >> (16 * y)) & 0xFFFF
            reversed_row = ((row & 0xF) << 12) | ((row & 0xF0) << 4) | ((row & 0xF00) >> 4) | ((row & 0xF000) >> 12)
            new_reversed_row = self.shift_row_int16_left(reversed_row)
            new_row = ((new_reversed_row & 0xF) << 12) | ((new_reversed_row & 0xF0) << 4) | ((new_reversed_row & 0xF00) >> 4) | ((new_reversed_row & 0xF000) >> 12)
            new_grid_int64 |= (new_row & 0xFFFF) << (16 * y)
        return new_grid_int64

    # shifting up = transpose, shift left, transpose again
    def shift_grid_up_int64(self, grid_int64):
        transposed = self.transpose_int64(grid_int64)
        shifted = self.shift_grid_left_int64(transposed)
        return self.transpose_int64(shifted)
    
    # shifting down = transpose, shift right, transpose again
    def shift_grid_down_int64(self, grid_int64):
        transposed = self.transpose_int64(grid_int64)
        shifted = self.shift_grid_right_int64(transposed)
        return self.transpose_int64(shifted)

    # shift a single row represented as a 16-bit integer to the left
    def shift_row_int16_left(self, row):
        # row is a 16-bit integer representing 4 tiles (4 bits each)
        tiles = [(row >> (4 * i)) & 0xF for i in range(4)]
        new_tiles = [t for t in tiles if t != 0]

        idx = 0
        while idx < len(new_tiles) - 1:
            if new_tiles[idx] == new_tiles[idx + 1]:
                new_tiles[idx] += 1
                del new_tiles[idx + 1]
            idx += 1

        new_tiles += [0] * (4 - len(new_tiles))
        new_row = 0
        for i in range(4):
            new_row |= (new_tiles[i] & 0xF) << (4 * i)
        return new_row
    
    def transpose_int64(self, grid_int64):
        transposed = 0
        for y in range(4):
            for x in range(4):
                value = (grid_int64 >> (4 * (y * 4 + x))) & 0xF
                transposed |= value << (4 * (x * 4 + y))
        return transposed

    # generate a score for the entire board by scoring each row and column
    def score_board(self, grid_int64):
        total_board_score = 0
        for i in range(4):
            row_int = (grid_int64 >> (16 * i)) & 0xFFFF
            col_int = 0
            for j in range(4):
                col_int |= ((grid_int64 >> (4 * (j * 4 + i))) & 0xF) << (4 * j)
            total_board_score += sum(self.get_row_score(row_int))
            total_board_score += sum(self.get_row_score(col_int))
        return total_board_score

    def get_row_score(self, row_int):
        # retrieve from cache if available
        if row_int in self.row_cache:
            return self.row_cache[row_int]
        
        # score a row based on sum of squares, higher values = higher score
        sum_score = 0

        # count of empty tiles
        empty_count = 0

        # number of possible merges in this row if shifted left or right
        merge_potential = 0

        # monotonicity score
        mono_left = 0
        mono_right = 0

        merge_counter = 0
        previous_tile = 0
        for i in range(4):
            this_tile = (row_int >> (4 * i)) & 0xF

            sum_score += pow(this_tile, SUM_SCALE)
            if this_tile == 0:
                empty_count += 1
            else:
                if this_tile == previous_tile:
                    merge_counter += 1
                elif merge_counter > 0:
                    merge_potential += 1 + merge_counter
                    merge_counter = 0

            if i > 0:
                if previous_tile > this_tile:
                    mono_left += pow(previous_tile, MONO_SCALE) - pow(this_tile, MONO_SCALE)
                else:
                    mono_right += pow(this_tile, MONO_SCALE) - pow(previous_tile, MONO_SCALE)

            previous_tile = this_tile

        if merge_counter > 0:
            merge_potential += 1 + merge_counter

        self.row_cache[row_int] = [
            BASE_SCORE, 
            -sum_score * SUM_WEIGHT, 
            empty_count * EMPTY_WEIGHT, 
            merge_potential * MERGE_WEIGHT, 
            -min(mono_left, mono_right) * MONO_WEIGHT
        ]
        return self.row_cache[row_int]
    
    def init_rows(self):
        for i in range(0x10000):
            self.get_row_score(i)