"""dp[i] = max(dp[i-1], dp[i-2] + nums[i]), kept in two rolling variables.

Time O(n), space O(1).
"""


class Solution:
    def rob(self, nums: List[int]) -> int:
        prev, curr = 0, 0  # best up to i-2, best up to i-1
        for num in nums:
            prev, curr = curr, max(curr, prev + num)
        return curr
