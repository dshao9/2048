import random


class Board:
    def __init__(self, board_size: int):
        self.size = board_size
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.board_changed = False

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.grid])
    
    def spawn_tile(self):
        empty_coords = [(x, y) for y in range(self.size) for x in range(self.size) if self.grid[y][x] == 0]
        if not empty_coords:
            return
        x, y = random.choice(empty_coords)
        self.grid[y][x] = 2 if random.random() < 0.9 else 4
        self.board_changed = False

    # used for testing
    def set_grid(self, new_grid):
        self.grid = new_grid

    def shift_left(self):
        for y in range(self.size):
            new_row = [i for i in self.grid[y] if i != 0]

            idx = 0
            while idx < len(new_row) - 1:
                if new_row[idx] == new_row[idx + 1]:
                    new_row[idx] += new_row[idx + 1]
                    self.score += new_row[idx]
                    del new_row[idx + 1]
                idx += 1

            new_row += [0] * (self.size - len(new_row))
            if new_row != self.grid[y]:
                self.board_changed = True
            self.grid[y] = new_row

    def shift_right(self):
        for y in range(self.size):
            new_row = [i for i in self.grid[y] if i != 0]
            
            idx = len(new_row) - 1
            while idx > 0:
                if new_row[idx] == new_row[idx - 1]:
                    new_row[idx] += new_row[idx - 1]
                    self.score += new_row[idx]
                    del new_row[idx - 1]
                    idx -= 1
                idx -= 1

            new_row = [0] * (self.size - len(new_row)) + new_row
            if new_row != self.grid[y]:
                self.board_changed = True
            self.grid[y] = new_row

    def shift_up(self):
        for x in range(self.size):
            new_col = [self.grid[y][x] for y in range(self.size) if self.grid[y][x] != 0]
            
            idx = 0
            while idx < len(new_col) - 1:
                if new_col[idx] == new_col[idx + 1]:
                    new_col[idx] += new_col[idx + 1]
                    self.score += new_col[idx]
                    del new_col[idx + 1]
                idx += 1

            new_col += [0] * (self.size - len(new_col))
            if new_col != [self.grid[y][x] for y in range(self.size)]:
                self.board_changed = True
            for y in range(self.size):
                self.grid[y][x] = new_col[y]

    def shift_down(self):
        for x in range(self.size):
            new_col = [self.grid[y][x] for y in range(self.size) if self.grid[y][x] != 0]
            
            idx = len(new_col) - 1
            while idx > 0:
                if new_col[idx] == new_col[idx - 1]:
                    new_col[idx] += new_col[idx - 1]
                    self.score += new_col[idx]
                    del new_col[idx - 1]
                idx -= 1

            new_col = [0] * (self.size - len(new_col)) + new_col
            if new_col != [self.grid[y][x] for y in range(self.size)]:
                self.board_changed = True
            for y in range(self.size):
                self.grid[y][x] = new_col[y]

    def can_move(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] == 0:
                    return True
                if x < self.size - 1 and self.grid[y][x] == self.grid[y][x + 1]:
                    return True
                if y < self.size - 1 and self.grid[y][x] == self.grid[y + 1][x]:
                    return True
        return False
    
    def is_2048(self):
        return any(2048 in row for row in self.grid)