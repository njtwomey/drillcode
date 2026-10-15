"""Perfect Squares (#279, medium)

Approach: Unbounded knapsack minimising count; dp[i] is the minimum of dp[i - sq] + 1
    over every square sq <= i.
Tricks: Greedy largest-square-first is wrong (12 is 4+4+4, not 9+1+1+1); dp[0] = 0 and
    others start at infinity.
Edge cases:
  - n itself a perfect square (1)
  - n = 1, 2, 3 (only ones)
  - Numbers needing four squares such as 7

Time O(n·√n), space O(n).
"""

class Solution:
    def numSquares(self, n: int) -> int:
        squares = [k * k for k in range(1, int(n**0.5) + 1)]
        # dp[i] = fewest perfect squares that sum to i.
        # Base case: dp[0] = 0 (empty sum). Every other entry starts at infinity; it is
        # always finite by the end because 1 is a square (i ones always works).
        dp = [0] + [float("inf")] * n

        # Loop order: i ascending, since dp[i] reads smaller indices dp[i - sq].
        for i in range(1, n + 1):
            for sq in squares:
                if sq > i:
                    break  # squares are sorted, so no later one fits either
                # Use one square of size sq, then finish the rest optimally.
                dp[i] = min(dp[i], dp[i - sq] + 1)
        return dp[n]
