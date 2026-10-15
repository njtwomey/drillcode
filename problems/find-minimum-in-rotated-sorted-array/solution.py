"""Binary search: if nums[mid] > nums[hi] the minimum is right of mid, else it is at mid or left.

Comparing with hi (not lo) handles the unrotated case with no special branch.
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
