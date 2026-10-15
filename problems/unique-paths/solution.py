"""Unique Paths (#62, medium)

Approach: dp[i][j] = dp[i-1][j] + dp[i][j-1], or one row updated in place.
Tricks: Closed form C(m + n - 2, m - 1) is a one-liner.
Edge cases:
  - 1xN or Nx1 grid (answer 1)

Time O(m·n), space O(n).
"""


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # row[j] holds the path count to the cell in column j of the current grid row.
        # First row is all 1s: there is only one way along the top edge.
        row = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                # row[j] still holds the cell above (previous row); row[j - 1] is the
                # cell to the left (already updated). Their sum is the new count.
                # Column 0 stays 1: only one way straight down the left edge.
                row[j] += row[j - 1]
        return row[-1]
