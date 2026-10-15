"""House Robber (#198, medium)

Approach: dp[i] = max(dp[i-1], dp[i-2] + nums[i]) with two rolling variables.
Edge cases:
  - One house
  - Two houses

Time O(n), space O(1).
"""


class Solution:
    def rob(self, nums: List[int]) -> int:
        prev, curr = 0, 0  # best up to i-2, best up to i-1
        # Each house: skip it (keep curr) or rob it (add to best up to two houses back).
        # Only two values are needed, so no full dp array.
        for num in nums:
            prev, curr = curr, max(curr, prev + num)
        return curr
