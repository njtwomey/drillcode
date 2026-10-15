"""Set Matrix Zeroes (#73, medium)

Approach: Use the first row and column as markers, with a separate flag for the first
    column itself.
Tricks: O(1) extra space needs the marker trick; zero the first row and column last.
Edge cases:
  - Zero in the first row or column
  - 1x1
  - All zeros

Time O(m·n), space O(1).
"""


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        rows, cols = len(matrix), len(matrix[0])
        first_row = any(matrix[0][c] == 0 for c in range(cols))
        first_col = any(matrix[r][0] == 0 for r in range(rows))
        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][c] == 0:
                    matrix[r][0] = 0
                    matrix[0][c] = 0
        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][0] == 0 or matrix[0][c] == 0:
                    matrix[r][c] = 0
        if first_row:
            for c in range(cols):
                matrix[0][c] = 0
        if first_col:
            for r in range(rows):
                matrix[r][0] = 0
