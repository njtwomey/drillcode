"""Minimum Path Sum (#64, medium)

Approach: Grid DP where each cell costs its value plus the smaller of the cell above and
    the cell to the left, kept in one rolling row.
Tricks: Seed a virtual start with 0 and everything else inf so the first row and column
    need no special code; greedy neighbour choice is wrong.
Edge cases:
  - Single cell, row or column
  - Zero-valued cells
  - A cheap-looking first step leading to an expensive cell

Time O(m·n), space O(n).
"""

class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        inf = float("inf")
        # dp[j] = cheapest cost to reach column j of the row being processed. Before the
        # first row, dp[j] still holds the answer for "the row above" (nothing reaches it,
        # so inf), except dp[0] = 0, a virtual start just above the top-left cell. That
        # base case makes the top-left cost exactly grid[0][0].
        dp = [inf] * cols
        dp[0] = 0

        # Loop order: rows top to bottom, columns left to right. When we reach (i, j),
        # dp[j] still holds the value from the row above (arrive moving down) and
        # dp[j - 1] was just updated for this row (arrive moving right).
        for i in range(rows):
            for j in range(cols):
                left = dp[j - 1] if j > 0 else inf
                dp[j] = min(dp[j], left) + grid[i][j]
        return dp[cols - 1]
