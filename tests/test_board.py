from board import Board

def test_shift_left_simple():
    board = Board(4)
    board.set_grid([[2, 0, 0, 0],
                    [0, 2, 0, 0],
                    [0, 0, 2, 0],
                    [0, 0, 0, 2]])
    board.shift_left()
    assert board.grid == [[2, 0, 0, 0],
                          [2, 0, 0, 0],
                          [2, 0, 0, 0],
                          [2, 0, 0, 0]]
    assert board.score == 0

def test_shift_left_merge():
    board = Board(4)
    board.set_grid([[2, 2, 0, 0],
                     [4, 4, 4, 4],
                     [2, 0, 2, 4],
                     [0, 0, 0, 0]])
    board.shift_left()
    assert board.grid == [[4, 0, 0, 0],
                          [8, 8, 0, 0],
                          [4, 4, 0, 0],
                          [0, 0, 0, 0]]
    assert board.score == 24

def test_shift_left_merge_2():
    board = Board(4)
    board.set_grid([[0, 8, 2, 2],
                     [4, 2, 0, 2],
                     [0, 0, 0, 0],
                     [0, 0, 0, 2]])
    board.shift_left()
    assert board.grid == [[8, 4, 0, 0],
                          [4, 4, 0, 0],
                          [0, 0, 0, 0],
                          [2, 0, 0, 0]]
    assert board.score == 8

def test_shift_left_no_change():
    board = Board(4)
    board.set_grid([[2, 4, 8, 16],
                     [0, 0, 0,  0],
                     [2, 4, 8, 16],
                     [0, 0, 0,  0]])
    before = [row[:] for row in board.grid]
    board.shift_left()
    assert board.grid == before
    assert board.score == 0

def test_shift_right_simple():
    board = Board(4)
    board.set_grid([[0, 0, 0, 2],
                    [0, 0, 2, 0],
                    [0, 2, 0, 0],
                    [2, 0, 0, 0]])
    board.shift_right()
    assert board.grid == [[0, 0, 0, 2],
                          [0, 0, 0, 2],
                          [0, 0, 0, 2],
                          [0, 0, 0, 2]]
    assert board.score == 0
    
def test_shift_right_merge():
    board = Board(4)
    board.set_grid([[0, 0, 2, 2],
                     [4, 4, 4, 4],
                     [2, 2, 0, 2],
                     [2, 0, 0, 0]])
    board.shift_right()
    assert board.grid == [[0, 0, 0, 4],
                          [0, 0, 8, 8],
                          [0, 0, 2, 4],
                          [0, 0, 0, 2]]
    assert board.score == 24

def test_shift_right_merge_2():
    board = Board(4)
    board.set_grid([[0, 8, 2, 2],
                     [4, 2, 0, 2],
                     [0, 0, 0, 0],
                     [0, 0, 0, 2]])
    board.shift_right()
    assert board.grid == [[0, 0, 8, 4],
                          [0, 0, 4, 4],
                          [0, 0, 0, 0],
                          [0, 0, 0, 2]]
    assert board.score == 8
    
def test_shift_right_no_change():
    board = Board(4)
    board.set_grid([[2, 4, 8, 16],
                     [0, 0, 0,  0],
                     [2, 4, 8, 16],
                     [0, 0, 0,  0]])
    before = [row[:] for row in board.grid]
    board.shift_right()
    assert board.grid == before
    assert board.score == 0

def test_shift_up_simple():
    board = Board(4)
    board.set_grid([[0, 0, 0, 2],
                    [0, 0, 2, 0],
                    [0, 2, 0, 0],
                    [2, 0, 0, 0]])
    board.shift_up()
    assert board.grid == [[2, 2, 2, 2],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]] 
    assert board.score == 0
    
def test_shift_up_merge():
    board = Board(4)
    board.set_grid([[2, 0, 2, 0],
                     [2, 4, 2, 4],
                     [0, 4, 0, 4],
                     [2, 0, 0, 4]])
    board.shift_up()
    assert board.grid == [[4, 8, 4, 8],
                          [2, 0, 0, 4],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]
    assert board.score == 24

def test_shift_up_merge_2():
    board = Board(4)
    board.set_grid([[0, 8, 2, 2],
                     [4, 2, 0, 2],
                     [0, 0, 0, 0],
                     [0, 0, 0, 2]])
    board.shift_up()
    assert board.grid == [[4, 8, 2, 4],
                          [0, 2, 0, 2],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]
    assert board.score == 4
    
def test_shift_up_no_change():
    board = Board(4)
    board.set_grid([[2, 0, 2, 0],
                     [4, 0, 4, 0],
                     [8, 0, 8, 0],
                    [16, 0, 16, 0]])
    before = [row[:] for row in board.grid]
    board.shift_up()
    assert board.grid == before
    assert board.score == 0

def test_shift_down_simple():
    board = Board(4)
    board.set_grid([[2, 0, 0, 0],
                    [0, 2, 0, 0],
                    [0, 0, 2, 0],
                    [0, 0, 0, 2]])
    board.shift_down()
    assert board.grid == [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [2, 2, 2, 2]]
    assert board.score == 0
    
def test_shift_down_merge():
    board = Board(4)
    board.set_grid([[2, 0, 2, 0],
                     [2, 4, 2, 4],
                     [0, 4, 0, 4],
                     [2, 0, 0, 4]])
    board.shift_down()
    assert board.grid == [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [2, 0, 0, 4],
                          [4, 8, 4, 8]]
    assert board.score == 24

def test_shift_down_merge_2():
    board = Board(4)
    board.set_grid([[0, 8, 2, 2],
                     [4, 2, 0, 2],
                     [0, 0, 0, 0],
                     [0, 0, 0, 2]])
    board.shift_down()
    assert board.grid == [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 8, 0, 2],
                          [4, 2, 2, 4]]
    assert board.score == 4

def test_shift_down_no_change():
    board = Board(4)
    board.set_grid([[2, 0, 2, 0],
                     [4, 0, 4, 0],
                     [8, 0, 8, 0],
                    [16, 0, 16, 0]])
    before = [row[:] for row in board.grid]
    board.shift_down()
    assert board.grid == before
    assert board.score == 0

def test_no_moves_left():
    board = Board(4)
    board.set_grid([[2, 4, 2, 4],
                     [4, 2, 4, 2],
                     [2, 4, 2, 4],
                     [4, 2, 4, 2]])
    assert not board.can_move()

def test_moves_left():
    board = Board(4)
    board.set_grid([[2, 8, 2, 8],
                     [4, 16, 8, 4],
                     [2, 2, 32, 8],
                     [4, 2, 8, 2]])
    assert board.can_move()

def test_moves_left_empty_space():
    board = Board(4)
    board.set_grid([[2, 4, 2, 4],
                     [4, 2, 4, 2],
                     [2, 4, 2, 4],
                     [4, 2, 4, 0]])
    assert board.can_move()

def test_moves_left_merge_y():
    board = Board(4)
    board.set_grid([[2, 4, 2, 4],
                     [4, 2, 4, 2],
                     [2, 4, 8, 4],
                     [4, 2, 16, 4]])
    assert board.can_move()

def test_moves_left_merge_x():
    board = Board(4)
    board.set_grid([[2, 4, 2, 4],
                     [4, 2, 4, 2],
                     [2, 16, 2, 4],
                     [4, 4, 8, 2]])
    assert board.can_move()

def test_spawn_tile():
    board = Board(4)
    board.set_grid([[2, 4, 2, 4],
                     [4, 2, 4, 2],
                     [2, 4, 2, 4],
                     [4, 2, 4, 0]])
    board.spawn_tile()
    non_empty_count = sum(1 for row in board.grid for val in row if val != 0)
    assert non_empty_count == 16
    assert board.grid[3][3] in (2, 4) # The new tile should be either 2 or 4

def test_spawn_tile_full_board():
    board = Board(4)
    board.set_grid([[2, 4, 2, 4],
                     [4, 2, 4, 2],
                     [2, 4, 2, 4],
                     [4, 2, 4, 2]])
    before = [row[:] for row in board.grid]
    board.spawn_tile()
    assert board.grid == before # No change since the board is full

def test_shift_up_merge_twice():
    board = Board(4)
    board.set_grid([[2, 0, 2, 2],
                     [2, 0, 2, 2],
                     [0, 0, 0, 0],
                     [4, 0, 4, 4]])
    board.shift_up()
    assert board.grid == [[4, 0, 4, 4], 
                           [4, 0, 4, 4], 
                           [0, 0, 0, 0], 
                           [0, 0, 0, 0]]
    assert board.score == 12
    board.shift_up()
    assert board.grid == [[8, 0, 8, 8],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]
    assert board.score == 36

def test_board_changed_flag():
    board = Board(4)
    board.set_grid([[2, 0, 0, 0],
                     [0, 2, 0, 0],
                     [0, 0, 2, 0],
                     [0, 0, 0, 2]])
    board.shift_left()
    assert board.board_changed
    board.board_changed = False
    board.shift_left()
    assert not board.board_changed

def test_board_changed_flag_no_merge():
    board = Board(4)
    board.set_grid([[2, 0, 0, 0],
                     [2, 0, 0, 0],
                     [2, 0, 0, 0],
                     [0, 0, 0, 0]])
    board.shift_left()
    assert not board.board_changed

def test_board_changed_flag_change():
    board = Board(4)
    board.set_grid([[2, 0, 0, 0],
                     [2, 0, 0, 0],
                     [0, 0, 2, 0],
                     [0, 0, 0, 0]])
    board.shift_left()
    assert board.board_changed

def test_board_changed_flag_merge():
    board = Board(4)
    board.set_grid([[32, 16, 8, 4],
                     [32, 16, 4, 2],
                     [8, 4, 0, 2],
                     [8, 0, 0, 0]])
    assert not board.board_changed
    board.shift_left()
    assert board.board_changed
    board.board_changed = False
    board.shift_left()
    assert board.grid == [[32, 16, 8, 4],
                           [32, 16, 4, 2],
                           [8, 4, 2, 0],
                           [8, 0, 0, 0]]
    assert not board.board_changed

def test_win_con():
    board = Board(4)
    board.set_grid([[2, 4, 2, 4],
                     [4, 2, 4, 2],
                     [2, 4, 2048, 4],
                     [4, 2, 4, 2]])
    assert board.is_2048()
    board.set_grid([[2, 4, 2, 4],
                     [4, 2, 4, 2],
                     [2, 4, 1024, 4],
                     [4, 2, 4, 2]])
    assert not board.is_2048()