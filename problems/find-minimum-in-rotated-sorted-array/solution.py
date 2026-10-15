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
        # Invariant: the minimum is always inside [lo, hi].
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            # Compare with hi, not lo: it tells us which side holds the rotation point
            # even when the range is already sorted (then nums[mid] <= nums[hi]).
            if nums[mid] > nums[hi]:
                # mid is above the right end, so the drop lies right of mid.
                lo = mid + 1
            else:
                # mid could itself be the min, so keep it (hi = mid, not mid - 1).
                hi = mid
        # lo == hi: the window shrank to the single minimum.
        return nums[lo]
