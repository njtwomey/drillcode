"""Unique Paths (#62, medium)

Approach: dp[i][j] = dp[i-1][j] + dp[i][j-1], or one row updated in place.
Tricks: Closed form C(m + n - 2, m - 1) is a one-liner.
Edge cases:
  - 1xN or Nx1 grid (answer 1)

Time O(m·n), space O(n).
"""


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        row = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                row[j] += row[j - 1]
        return row[-1]
