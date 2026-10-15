"""Unbounded knapsack: dp[a] = min over coins of dp[a - c] + 1, with dp[0] = 0.

Initialised with amount + 1 (an unreachable sentinel) instead of infinity.
Time O(amount * coins), space O(amount).
"""


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [0] + [amount + 1] * amount
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1
        return dp[amount] if dp[amount] <= amount else -1
