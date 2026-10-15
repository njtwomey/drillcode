"""Burst Balloons (#312, hard)

Approach: Interval DP over a list padded with 1s, choosing the last balloon k burst in
    each open interval (l, r).
Tricks: Pick the last balloon, not the first, so its neighbours are fixed at l and r and
    the two sides are independent; pad both ends with 1.
Edge cases:
  - Single balloon
  - Empty input (0)
  - Zeros among the values

Time O(n³), space O(n²).
"""

class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        # Sentinel 1s on both ends: a balloon at the edge is multiplied by an imaginary 1.
        # An empty input becomes [1, 1] and correctly scores 0.
        vals = [1] + nums + [1]
        size = len(vals)

        # dp[l][r] = most coins from bursting every balloon strictly between l and r, where
        # balloons l and r themselves stay in place until the end.
        # Base case: dp[l][l+1] = 0 (nothing lies between neighbours), the default zero.
        dp = [[0] * size for _ in range(size)]

        # Think of k as the LAST balloon burst in (l, r). When it goes, only l and r remain
        # beside it, so its score is vals[l] * vals[k] * vals[r], independent of how the
        # two sides were popped. The left and right sides become independent subproblems.
        # (Choosing the FIRST balloon instead would leave neighbours that depend on later
        # choices.)
        # Loop order: by interval length (gap = r - l) increasing, because dp[l][r] reads
        # dp[l][k] and dp[k][r], which are strictly shorter.
        for gap in range(2, size):
            for l in range(size - gap):
                r = l + gap
                for k in range(l + 1, r):
                    coins = vals[l] * vals[k] * vals[r] + dp[l][k] + dp[k][r]
                    dp[l][r] = max(dp[l][r], coins)
        return dp[0][size - 1]
