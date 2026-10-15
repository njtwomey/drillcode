"""Combination Sum IV (#377, medium)

Approach: dp[t] = sum over nums of dp[t - n], dp[0] = 1, with the target loop outermost.
Tricks: This counts ordered sequences; Coin Change II puts the coin loop outermost to
    count unordered ones.
Edge cases:
  - Target 0
  - Large counts (fit in 32 bits by the constraints)

Time O(target · n), space O(target).
"""


class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        dp = [1] + [0] * target
        for t in range(1, target + 1):
            for n in nums:
                if n <= t:
                    dp[t] += dp[t - n]
        return dp[target]
