"""House Robber II (#213, medium)

Approach: Run House Robber on houses 0..n-2 and on 1..n-1; take the larger.
Tricks: The circle makes the first and last house mutually exclusive, so split into two
    linear problems.
Edge cases:
  - Single house (neither run covers it
  - Return it directly)
  - Two houses

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
