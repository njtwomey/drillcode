"""Minimum Size Subarray Sum (#209, medium)

Approach: Expand right adding to a running sum; while the sum reaches target, record the
    length and shrink from the left.
Tricks: Positivity makes the window monotone, so each pointer only moves forward; return
    0 if best never improved.
Edge cases:
  - No subarray reaches target
  - A single element suffices
  - Whole array needed

Time O(n), space O(1).
"""

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        # All numbers are positive, so growing the window only raises the sum and
        # shrinking only lowers it. That monotonicity is what makes two pointers valid.
        left = 0
        total = 0
        best = len(nums) + 1  # impossible length, doubles as the "not found" marker
        for right, num in enumerate(nums):
            total += num
            # Window [left, right] is big enough: shrink it from the left for as long as it
            # stays big enough, recording the shortest length seen along the way.
            while total >= target:
                best = min(best, right - left + 1)
                total -= nums[left]
                left += 1
        return 0 if best > len(nums) else best
