"""Coin Change II (#518, medium)

Approach: Unbounded knapsack counting; for each coin in an outer loop, add dp[a - coin]
    into dp[a] for a ascending.
Tricks: Coins outside and amounts inside counts combinations; swapping the loops would
    count permutations.
Edge cases:
  - Amount 0 (one way, the empty set)
  - Amount not reachable (0)
  - Coin larger than the amount

Time O(n·amount), space O(amount).
"""

class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        # dp[a] = number of coin multisets (order ignored) that sum to a, using only the
        # coins processed so far.
        # Base case: dp[0] = 1, the empty selection makes amount 0. This is also why
        # amount = 0 returns 1.
        dp = [0] * (amount + 1)
        dp[0] = 1

        # Loop order matters. Coins form the OUTER loop, so each combination is built in the
        # order of the coin list and counted once. Swapping the loops would count 1+2 and
        # 2+1 separately (permutations). The amount loop runs upward because a coin may be
        # reused: dp[a - coin] may already include this very coin.
        for coin in coins:
            for a in range(coin, amount + 1):
                dp[a] += dp[a - coin]
        return dp[amount]
