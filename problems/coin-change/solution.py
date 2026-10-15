"""Coin Change (#322, medium)

Approach: dp[a] = min over coins of dp[a - c] + 1, with dp[0] = 0.
Tricks: Unbounded knapsack; initialise with amount + 1 rather than infinity to simplify
    the final check.
Edge cases:
  - Amount 0 (answer 0)
  - Impossible amount (answer -1)
  - Every coin larger than the amount

Time O(amount · coins), space O(amount).
"""


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [0] + [amount + 1] * amount
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1
        return dp[amount] if dp[amount] <= amount else -1
