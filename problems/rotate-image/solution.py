"""Rotate Image (#48, medium)

Approach: Transpose, then reverse each row, for clockwise.
Tricks: Counter-clockwise is transpose then reverse each column.
Edge cases:
  - 1x1
  - 2x2

Time O(n²), space O(1).
"""

# Judge notes:
# Do not return anything: modify matrix in place instead.


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        # Step 1: transpose (reflect over the main diagonal), so (i, j) -> (j, i).
        # Starting j at i + 1 visits each pair once; swapping the whole square would
        # undo itself, and the diagonal does not move.
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # Step 2: reversing each row mirrors left to right. Transpose plus mirror
        # equals a 90 degree clockwise turn, done in place with no second matrix.
        for row in matrix:
            row.reverse()
