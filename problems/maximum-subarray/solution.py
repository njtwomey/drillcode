"""Maximum Subarray (#53, medium)

Approach: cur = max(num, cur + num); best = max(best, cur).
Tricks: Kadane's algorithm; the divide-and-conquer version is a listed follow-up.
Edge cases:
  - All negative (answer is the largest single element)
  - Single element

Time O(n), space O(1).
"""


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        cur = best = nums[0]
        for num in nums[1:]:
            cur = max(num, cur + num)
            best = max(best, cur)
        return best
