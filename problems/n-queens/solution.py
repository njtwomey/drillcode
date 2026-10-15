"""N-Queens (#51, hard)

Approach: Place one queen per row, tracking used columns and both diagonals in sets.
Tricks: Cells on one diagonal share row - col and on the other share row + col, so three
    sets give O(1) conflict checks.
Edge cases:
  - n = 1
  - n = 2 and n = 3 have no solution
  - Undo all three sets when backtracking

Time O(n!), space O(n).
"""

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        result = []
        path = []  # path[row] = column of the queen placed in that row
        # One queen per row is built in by placing row by row. These sets record which
        # columns and diagonals are taken: cells on one "\" diagonal share row - col,
        # cells on one "/" diagonal share row + col.
        cols, diag, anti = set(), set(), set()

        def backtrack(row: int) -> None:
            if row == n:
                result.append(["." * col + "Q" + "." * (n - col - 1) for col in path])
                return
            for col in range(n):
                if col in cols or row - col in diag or row + col in anti:
                    continue
                cols.add(col)
                diag.add(row - col)
                anti.add(row + col)
                path.append(col)
                backtrack(row + 1)
                path.pop()
                cols.remove(col)
                diag.remove(row - col)
                anti.remove(row + col)

        backtrack(0)
        return result
