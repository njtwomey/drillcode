"""Triangle (#120, medium)

Approach: Bottom-up from the last row, replacing each cell by its value plus the smaller
    of its two children, reusing one array.
Tricks: Going bottom-up leaves the answer in dp[0] and avoids ragged edge handling; copy
    the last row so the input is not mutated.
Edge cases:
  - Single row
  - Negative values
  - A locally cheaper child that leads to a worse path

Time O(n²), space O(n).
"""

class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        # dp[j] = cheapest path sum from the cell (current row, j) down to the bottom.
        # Base case: the bottom row, whose cost is just its own values.
        # Working bottom-up means the answer lands in a single cell, dp[0], and every row
        # has exactly the children it needs below it (row i has one more entry than row
        # i-1, so cell j has children j and j+1). Going top-down would need separate
        # handling of the ragged edges and a final min over the last row.
        dp = triangle[-1][:]  # copy so the input is not modified

        # Loop order: rows from the second-to-last upward; within a row, left to right is
        # safe because dp[j] is replaced using dp[j] and dp[j + 1], which are not yet
        # overwritten for this row.
        for i in range(len(triangle) - 2, -1, -1):
            for j in range(i + 1):
                dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
        return dp[0]
