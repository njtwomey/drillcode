"""dp[i] = dp[i >> 1] + (i & 1), filled in increasing order from dp[0] = 0.

Time O(n), space O(n).
"""


class Solution:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp

    # Alternative: drop the lowest set bit and add one.
    def countBitsLowbit(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i & (i - 1)] + 1
        return dp
