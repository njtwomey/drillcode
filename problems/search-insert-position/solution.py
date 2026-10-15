"""Search Insert Position (#35, easy)

Approach: Lower-bound binary search over [0, n) returning the first index with
    nums[index] >= target.
Tricks: Start hi at len(nums), not len(nums) - 1, so appending at the end is reachable.
Edge cases:
  - Target larger than every element (returns len(nums))
  - Target smaller than every element (returns 0)
  - Single element

Time O(log n), space O(1).
"""

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        # Lower bound: the first index whose value is >= target. That is the target's own
        # position if present, otherwise exactly where it would be inserted.
        # hi starts at len(nums), not len(nums) - 1, because "after everything" is a
        # legal answer.
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1  # mid and everything left of it are too small
            else:
                hi = mid  # mid could be the answer, so keep it in range
        return lo
