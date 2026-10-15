"""Search in Rotated Sorted Array (#33, medium)

Approach: Binary search; decide which of [lo, mid] or [mid, hi] is sorted and whether
    the target lies in it.
Tricks: Exactly one half is sorted at every step; test the target against that half's
    bounds.
Edge cases:
  - Not rotated
  - Single element
  - Target at the pivot

Time O(log n), space O(1).
"""


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            # The rotation point lies in only one half, so at least one half is
            # fully sorted. Find it, then check whether target is inside its range.
            # <= (not <) so a one-element left half counts as sorted.
            if nums[lo] <= nums[mid]:  # left half sorted
                # Bounds are exclusive at mid because mid was already ruled out.
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1  # not in the sorted half, so must be in the other
            else:  # right half sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1
