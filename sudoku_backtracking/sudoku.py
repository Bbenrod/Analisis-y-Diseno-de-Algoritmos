"""Solve regular Sudoku puzzles using backtracking."""

LEFT_SUDOKU = [
    [5, 0, 0, 9, 1, 3, 7, 2, 0],
    [3, 0, 0, 0, 8, 0, 5, 0, 9],
    [0, 9, 0, 2, 5, 0, 0, 8, 0],
    [6, 8, 0, 4, 7, 0, 2, 3, 0],
    [0, 0, 9, 5, 0, 0, 4, 6, 0],
    [7, 0, 4, 0, 0, 0, 0, 0, 5],
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 8, 9, 1, 6, 0, 0],
    [8, 5, 0, 7, 2, 0, 0, 0, 3],
]

RIGHT_SUDOKU = [
    [6, 9, 0, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 9, 6, 0, 0, 0],
    [0, 8, 0, 7, 5, 3, 0, 9, 0],
    [0, 2, 0, 3, 7, 4, 5, 6, 1],
    [3, 6, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 0, 9, 6, 0, 3, 7, 8],
    [0, 0, 6, 0, 3, 1, 0, 8, 4],
    [0, 4, 5, 8, 0, 7, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 7],
]


def find_empty(board: list[list[int]]) -> tuple[int, int] | None:
    """Returns the first empty cell (row, column), or None.

    Pseudocode:
        Traverse rows and columns in order.
        If a cell contains 0, return its coordinates.
        If no empty cell is found, return None.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i,j)

    return None


def is_valid(board: list[list[int]], row: int, column: int, number: int) -> bool:
    """Checks whether number (1..9) can be placed in an empty cell.

    Pseudocode:
        If number occurs in the row, return false.
        If number occurs in the column, return false.
        Find the starting coordinates of the cell's 3×3 box.
        If number occurs in that box, return false.
        Return true.
    """
    for i in range(9):
        # Check the row
        if board[row][i] == number:
            return False

        # Check the column
        if board[i][column] == number:
            return False

    start_row = (row // 3) * 3
    start_column = (column // 3) * 3

    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_column + j] == number:
                return False

    return True


def solve_sudoku(board: list[list[int]]) -> bool:
    """Solves the board in place and returns whether a solution was found.

    Precondition: a 9×9 board with integers 0..9 and non-conflicting clues.
    If no solution exists, restore the original board.

    Pseudocode:
        Find an empty cell.
        If none exists, return true.
        For each number from 1 to 9:
            If placing it in the cell is valid:
                Place it temporarily.
                Recursively solve the rest of the board.
                If solved, return true.
                Reset the cell to 0 (backtrack).
        Return false.
    """
    current = find_empty(board)
    if current == None:
        return True

    row, column = current

    for number in range(1, 10):
        if is_valid(board, row, column, number):
            board[row][column] = number  # Place temporarily
            if solve_sudoku(board):
                return True
            else:
                board[row][column] = 0

    return False

if __name__ == "__main__":
    for name, original in (
        ("Case 1: Left Sudoku", LEFT_SUDOKU),
        ("Case 2: Right Sudoku", RIGHT_SUDOKU),
    ):
        board = [row[:] for row in original]
        print(name)
        try:
            solved = solve_sudoku(board)
        except NotImplementedError as error:
            print(f"Pending: {error}\n")
            continue
        if solved:
            for row in board:
                print(" ".join(map(str, row)))
        else:
            print("No solution")
        print()
