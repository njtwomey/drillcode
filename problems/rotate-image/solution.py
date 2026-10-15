"""Rotate Image (#48, medium)

Approach: Transpose, then reverse each row, for clockwise.
Tricks: Counter-clockwise is transpose then reverse each column.
Edge cases:
  - 1x1
  - 2x2

Time O(n²), space O(1).
"""


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        for row in matrix:
            row.reverse()
