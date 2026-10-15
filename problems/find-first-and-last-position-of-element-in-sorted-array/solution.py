"""Find First and Last Position of Element in Sorted Array (#34, medium)

Approach: Two lower-bound searches; first = lower_bound(target), last =
    lower_bound(target + 1) - 1.
Tricks: Reuse one lower-bound helper for both ends instead of writing two fiddly
    boundary searches.
Edge cases:
  - Empty array
  - Target absent (including above or below every element)
  - Whole array equals target
  - Single occurrence

Time O(log n), space O(1).
"""

class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # First index whose value is >= x (len(nums) if there is none).
        def lower_bound(x: int) -> int:
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = (lo + hi) // 2
                if nums[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        first = lower_bound(target)
        # Either target is bigger than everything, or the slot it would occupy holds
        # something else, so it is not in the array.
        if first == len(nums) or nums[first] != target:
            return [-1, -1]
        # Integers: the first element > target sits right after the last copy of target.
        last = lower_bound(target + 1) - 1
        return [first, last]
