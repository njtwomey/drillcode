"""Find Minimum in Rotated Sorted Array (#153, medium)

Approach: If nums[mid] > nums[hi] the minimum is right of mid, otherwise it is at mid or
    left.
Tricks: Comparing with hi rather than lo handles the unrotated case without a special
    branch.
Edge cases:
  - Not rotated
  - Two elements
  - Single element

Time O(log n), space O(1).
"""


class Solution:
    def findMin(self, nums: List[int]) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1
            else:
                hi = mid
        return nums[lo]
