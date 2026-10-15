"""Kadane's algorithm: cur = max(num, cur + num); best = max(best, cur).

Time O(n), space O(1).
"""


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        cur = best = nums[0]
        for num in nums[1:]:
            cur = max(num, cur + num)
            best = max(best, cur)
        return best
