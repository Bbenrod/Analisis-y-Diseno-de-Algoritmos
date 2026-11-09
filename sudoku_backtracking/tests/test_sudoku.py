import unittest

from sudoku_backtracking.sudoku import (
    RIGHT_SUDOKU,
    LEFT_SUDOKU,
    find_empty,
    is_valid,
    solve_sudoku,
)


# Auxiliary board independent of the assignment puzzles.
SOLVED_BOARD = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8],
]


class TestFindEmpty(unittest.TestCase):
    def test_first_in_order(self):
        self.assertEqual(find_empty(LEFT_SUDOKU), (0, 1))

    def test_complete(self):
        self.assertIsNone(find_empty(SOLVED_BOARD))

    def test_last_cell(self):
        board = [row[:] for row in SOLVED_BOARD]
        board[8][8] = 0
        self.assertEqual(find_empty(board), (8, 8))

    def test_empty(self):
        self.assertEqual(find_empty([[0] * 9 for _ in range(9)]), (0, 0))


class TestIsValid(unittest.TestCase):
    def test_conflicts_and_valid_candidate(self):
        # Each clue isolates one constraint for cell (4, 4).
        for clue, expected in [((4, 8), False), ((8, 4), False),
                                ((3, 3), False), ((0, 0), True)]:
            with self.subTest(clue=clue):
                board = [[0] * 9 for _ in range(9)]
                board[clue[0]][clue[1]] = 5
                original = [row[:] for row in board]
                self.assertIs(is_valid(board, 4, 4, 5), expected)
                self.assertEqual(board, original)

    def test_bottom_right_box(self):
        board = [[0] * 9 for _ in range(9)]
        board[6][6] = 9
        self.assertIs(is_valid(board, 8, 8, 9), False)


class TestSolveSudoku(unittest.TestCase):
    def assert_solved(self, original):
        board = [row[:] for row in original]
        self.assertIs(solve_sudoku(board), True)
        numbers = set(range(1, 10))
        self.assertEqual(len(board), 9)
        for row in board:
            self.assertEqual(len(row), 9)
            self.assertEqual(set(row), numbers)
        for column in zip(*board):
            self.assertEqual(set(column), numbers)
        for start_row in (0, 3, 6):
            for start_column in (0, 3, 6):
                box = [board[f][c]
                          for f in range(start_row, start_row + 3)
                          for c in range(start_column, start_column + 3)]
                self.assertEqual(set(box), numbers)
        for f in range(9):
            for c in range(9):
                if original[f][c] != 0:
                    self.assertEqual(board[f][c], original[f][c])

    def test_left_case(self):
        self.assert_solved(LEFT_SUDOKU)

    def test_right_case(self):
        self.assert_solved(RIGHT_SUDOKU)

    def test_already_solved(self):
        self.assert_solved(SOLVED_BOARD)

    def test_one_empty_cell(self):
        board = [row[:] for row in SOLVED_BOARD]
        board[8][8] = 0
        self.assert_solved(board)

    def test_empty_board(self):
        self.assert_solved([[0] * 9 for _ in range(9)])

    def test_unsolvable_restores_board(self):
        # Clues do not conflict, but row 0 requires 1 at (0, 0), blocked by its column.
        board = [[0, 2, 3, 4, 5, 6, 7, 8, 9],
                   [0] * 9, [0] * 9, [1] + [0] * 8,
                   *[[0] * 9 for _ in range(5)]]
        original = [row[:] for row in board]
        self.assertIs(solve_sudoku(board), False)
        self.assertEqual(board, original)


if __name__ == "__main__":
    unittest.main()
