from ai import AI

def test_ai_get_row_score():
    ai = AI()
    row = 0b0000_0000_0000_0000
    score = ai.get_row_score(row)
    assert score == [200000, -0.0, 1080, 0, 0]

    row = 0x0001
    score = ai.get_row_score(row)
    # sum_score = 1^2 * 1 = 1
    # empty_count = 3
    # merge_potential = 0
    assert score == [200000, -11.0, 810, 0, 0]

    row = 0x0011
    score = ai.get_row_score(row)
    # sum_score = 1^2 * 2 = 2
    # empty_count = 2
    # merge_potential = 2
    assert score == [200000, -22.0, 540, 1400, 0]

    row = 0x0111
    score = ai.get_row_score(row)
    # sum_score = 1^2 * 3 = 3
    # empty_count = 1
    # merge_potential = 3
    assert score == [200000, -33.0, 270, 2100, 0]

    row = 0x1111
    score = ai.get_row_score(row)
    # sum_score = 1^2 * 4 = 4
    # empty_count = 0
    # merge_potential = 4
    assert score == [200000, -44.0, 0, 2800, 0]

    row = 0b0010_0010_0010_0010
    score = ai.get_row_score(row)
    # sum_score = 2^2 * 4 = 16
    # empty_count = 0
    # merge_potential = 4
    assert score == [200000, -497.8031739553295, 0, 2800, 0]

    row = 0x3333
    score = ai.get_row_score(row)
    # sum_score = 3^2 * 4 = 36
    # empty_count = 0
    # merge_potential = 4
    assert score == [200000, -2057.6763593918263, 0, 2800, 0]

    row = 0x4444
    score = ai.get_row_score(row)
    # sum_score = 4^2 * 4 = 64
    # empty_count = 0
    # merge_potential = 4
    assert score == [200000, -5632.0, 0, 2800, 0]

    row = 0x1234
    score = ai.get_row_score(row)
    assert score == [200000, -2057.869883336789, 0, 0, 0]

    row = 0x3241
    score = ai.get_row_score(row)
    assert score == [200000, -2057.869883336789, 0, 0, -11280]

def test_ai_score_board():
    ai = AI()

    grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    int64_grid = ai.grid_to_int64(grid)
    score = ai.score_board(int64_grid)
    expected_score = 1608640.0
    assert score == expected_score

    grid = [[2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2]]
    int64_grid = ai.grid_to_int64(grid)
    score = ai.score_board(int64_grid)
    expected_score = 1622048.0
    assert score == expected_score

    grid = [[4, 4, 4, 4],
            [4, 4, 4, 4],
            [4, 4, 4, 4],
            [4, 4, 4, 4]]
    int64_grid = ai.grid_to_int64(grid)
    score = ai.score_board(int64_grid)
    expected_score = 1618417.5746083574
    assert score == expected_score
    
    grid = [[2, 2, 2, 2], # -> 8
            [4, 4, 4, 4], # -> 20
            [8, 8, 8, 8], # -> 40
            [16, 16, 16, 16]] # -> 68
            # ^30
    int64_grid = ai.grid_to_int64(grid)
    score = ai.score_board(int64_grid)
    expected_score = 1594737.0409333056
    assert score == expected_score

def test_grid_to_int64_empty():
    ai = AI()
    # Test converting a 4x4 grid to a 64-bit integer and back
    grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    int64_grid = ai.grid_to_int64(grid)
    expected_int = 0b0000
    assert int64_grid == expected_int

    grid = ai.int64_to_grid(int64_grid)
    expected_grid = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
    assert grid == expected_grid

def test_grid_to_int64_2():
    ai = AI()
    grid = [[2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    int64_grid = ai.grid_to_int64(grid)
    expected_int = 0b0001
    assert int64_grid == expected_int

    grid = ai.int64_to_grid(int64_grid)
    expected_grid = [[2, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
    assert grid == expected_grid

def test_grid_to_int64_4():
    ai = AI()
    grid = [[4, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    int64_grid = ai.grid_to_int64(grid)
    expected_int = 0b0010
    assert int64_grid == expected_int

    grid = ai.int64_to_grid(int64_grid)
    expected_grid = [[4, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
    assert grid == expected_grid

def test_grid_to_int64_full_2():
    ai = AI()
    grid = [[2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2],
            [2, 2, 2, 2]]
    int64_grid = ai.grid_to_int64(grid)
    expected_int = 0b0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001_0001
    assert int64_grid == expected_int

    grid = ai.int64_to_grid(int64_grid)
    expected_grid = [[2, 2, 2, 2],
                     [2, 2, 2, 2],
                     [2, 2, 2, 2],
                     [2, 2, 2, 2]]
    assert grid == expected_grid


def test_transpose_int64():
    ai = AI()

    original_grid = [[2, 4, 8, 16],
                     [32, 64, 128, 256],
                     [512, 1024, 2048, 4096],
                     [8192, 16384, 32768, 0]]
    int64_grid = ai.grid_to_int64(original_grid)
    transposed_int64 = ai.transpose_int64(int64_grid)
    transposed_grid = ai.int64_to_grid(transposed_int64)
    expected_transposed = [[2, 32, 512, 8192],
                           [4, 64, 1024, 16384],
                           [8, 128, 2048, 32768],
                           [16, 256, 4096, 0]]
    assert transposed_grid == expected_transposed


def test_shift_grid_left_int64():
    ai = AI()

    original_grid = [[2, 2, 4, 0],
                     [4, 4, 4, 4],
                     [2, 0, 2, 2],
                     [0, 0, 0, 2]]
    int64_grid = ai.grid_to_int64(original_grid)
    shifted_int64 = ai.shift_grid_left_int64(int64_grid)
    shifted_grid = ai.int64_to_grid(shifted_int64)
    expected_shifted = [[4, 4, 0, 0],
                        [8, 8, 0, 0],
                        [4, 2, 0, 0],
                        [2, 0, 0, 0]]
    assert shifted_grid == expected_shifted

def test_shift_grid_right_int64():
    ai = AI()

    original_grid = [[2, 2, 4, 0],
                     [4, 4, 4, 4],
                     [2, 0, 2, 2],
                     [0, 0, 0, 2]]
    int64_grid = ai.grid_to_int64(original_grid)
    shifted_int64 = ai.shift_grid_right_int64(int64_grid)
    shifted_grid = ai.int64_to_grid(shifted_int64)
    expected_shifted = [[0, 0, 4, 4],
                        [0, 0, 8, 8],
                        [0, 0, 2, 4],
                        [0, 0, 0, 2]]
    assert shifted_grid == expected_shifted

def test_shift_grid_up_int64():
    ai = AI()

    original_grid = [[2, 2, 4, 4],
                     [4, 4, 4, 4],
                     [2, 0, 2, 2],
                     [0, 0, 0, 2]]
    int64_grid = ai.grid_to_int64(original_grid)
    shifted_int64 = ai.shift_grid_up_int64(int64_grid)
    shifted_grid = ai.int64_to_grid(shifted_int64)
    expected_shifted = [[2, 2, 8, 8],
                        [4, 4, 2, 4],
                        [2, 0, 0, 0],
                        [0, 0, 0, 0]]
    assert shifted_grid == expected_shifted

def test_shift_grid_down_int64():
    ai = AI()

    original_grid = [[2, 2, 4, 4],
                     [4, 4, 4, 4],
                     [2, 0, 2, 2],
                     [0, 0, 0, 2]]
    int64_grid = ai.grid_to_int64(original_grid)
    shifted_int64 = ai.shift_grid_down_int64(int64_grid)
    shifted_grid = ai.int64_to_grid(shifted_int64)
    expected_shifted = [[0, 0, 0, 0],
                        [2, 0, 0, 0],
                        [4, 2, 8, 8],
                        [2, 4, 2, 4]]
    assert shifted_grid == expected_shifted