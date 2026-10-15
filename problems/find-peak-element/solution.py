"""Find Peak Element (#162, medium)

Approach: Binary search on the slope; if nums[mid] < nums[mid + 1] a peak lies right of
    mid, otherwise at mid or left.
Tricks: The out-of-range neighbours count as negative infinity, so a peak is guaranteed
    on whichever side the slope rises toward.
Edge cases:
  - Single element
  - Strictly increasing or decreasing array
  - Several peaks (any is valid)

Time O(log n), space O(1).
"""

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        # Invariant: [lo, hi] always contains a peak. Both outer neighbours are treated as
        # -infinity, so the edges of the window can never rule a peak out.
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < nums[mid + 1]:
                # Rising slope: walking right must either keep climbing to a peak or hit
                # the end of the array, which counts as a peak. mid itself is not one.
                lo = mid + 1
            else:
                # Falling slope (neighbours are distinct): mid or something left of it
                # is a peak, so keep mid in the window.
                hi = mid
        return lo
