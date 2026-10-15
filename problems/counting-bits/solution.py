"""Counting Bits (#338, easy)

Approach: dp[i] = dp[i >> 1] + (i & 1), filled in order from 0.
Tricks: dp[i] = dp[i & (i - 1)] + 1 also works: drop the lowest set bit and add one.
Edge cases:
  - n = 0

Time O(n), space O(n).
"""


class Solution:
    def countBits(self, n: int) -> List[int]:
        # dp[i] = number of 1 bits in i. dp[0] = 0 is the base case.
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            # i >> 1 is i without its last bit, and it is smaller, so it is already computed.
            # i & 1 is that last bit: add 1 if it was set. Each entry is O(1), so O(n) total.
            dp[i] = dp[i >> 1] + (i & 1)
        return dp

    # Alternative: drop the lowest set bit and add one.
    def countBitsLowbit(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            # i & (i - 1) clears the lowest set bit, giving a smaller number with one fewer 1.
            dp[i] = dp[i & (i - 1)] + 1
        return dp
