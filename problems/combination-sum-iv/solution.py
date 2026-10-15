"""dp[t] = sum of dp[t - n] over nums, dp[0] = 1, with the target loop outermost.

That order counts ordered sequences (Coin Change II swaps the loops to count unordered ones).
Time O(target * n), space O(target).
"""


class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        dp = [1] + [0] * target
        for t in range(1, target + 1):
            for n in nums:
                if n <= t:
                    dp[t] += dp[t - n]
        return dp[target]
