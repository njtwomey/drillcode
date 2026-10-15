"""Binary Search (#704, easy)

Approach: Standard lo/hi loop comparing the target with mid.
Tricks: Be consistent about whether hi is inclusive; lo + (hi - lo) // 2 avoids overflow
    in fixed-width languages.
Edge cases:
  - Empty array
  - Target below the first or above the last element
  - Single element

Time O(log n), space O(1).
"""


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # Inclusive bounds: the target, if present, is always within nums[lo..hi].
        lo, hi = 0, len(nums) - 1
        while lo <= hi:  # <= so a single remaining element (lo == hi) is still checked.
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            # mid is ruled out, so step past it (+1/-1); otherwise the loop could stall.
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1  # The window emptied (lo > hi) without finding target.
