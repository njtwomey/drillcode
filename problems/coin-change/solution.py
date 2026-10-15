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
        # dp[a] = fewest coins making amount a. amount + 1 acts as infinity, since no
        # valid answer can need more than `amount` coins (all 1s). dp[0] = 0 coins.
        dp = [0] + [amount + 1] * amount
        for a in range(1, amount + 1):
            # Last coin used is c, so the best is 1 + dp[a - c]; try every coin.
            # Cost is O(amount * len(coins)).
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1
        # Still the sentinel means unreachable.
        return dp[amount] if dp[amount] <= amount else -1
