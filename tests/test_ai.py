from board import Board
from ai import AI

def test_ai_get_row_score():
    ai = AI()
    # Test a row with merges and empty tiles
    row = [0] * 4
    score = ai.get_row_score(row)
    assert score == 4

    row = [2] * 4
    score = ai.get_row_score(row)
    # sum_score = 2^2 * 4 = 16
    # merge_potential = 3
    # empty_count = 0
    assert score == 20
