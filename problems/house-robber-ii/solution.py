"""The circle makes the first and last houses mutually exclusive, so run linear House Robber
on nums[:-1] and nums[1:] and take the larger; a single house is returned directly.

Time O(n), space O(1).
"""


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def rob_line(houses):
            prev, curr = 0, 0
            for num in houses:
                prev, curr = curr, max(curr, prev + num)
            return curr

        return max(rob_line(nums[:-1]), rob_line(nums[1:]))
