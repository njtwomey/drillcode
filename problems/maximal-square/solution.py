"""Maximal Square (#221, medium)

Approach: dp[i][j] is the side of the biggest all-ones square ending at that corner,
    equal to min(up, left, diagonal) + 1 on a "1".
Tricks: Pad a zero row and column so borders need no special case, compare cells to the
    string "1", and return side squared rather than side.
Edge cases:
  - All zeros (0)
  - Single row or column
  - Rectangle of ones that is not a square

Time O(m·n), space O(m·n).
"""

class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        rows, cols = len(matrix), len(matrix[0])
        # dp[i][j] = side length of the largest square of all "1"s whose bottom-right
        # corner is cell (i-1, j-1) of the matrix. The table has one extra row and column
        # of zeros on the top and left as the base case: a corner on the border can only
        # be a 1x1 square, and the padding gives min(...) + 1 = 1 without special cases.
        dp = [[0] * (cols + 1) for _ in range(rows + 1)]
        best = 0

        # Loop order: row-major, since each cell reads its upper, left and upper-left cells.
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if matrix[i - 1][j - 1] == "1":
                    # A square of side k ending here needs squares of side k-1 ending at
                    # the three neighbours; the smallest of them limits the growth.
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                    best = max(best, dp[i][j])
        return best * best  # the answer is an area
