"""3Sum Closest (#16, medium)

Approach: Sort, fix the first element, and sweep the rest with two pointers, tracking
    the sum nearest the target.
Tricks: Move left when the sum is below target and right when above; return immediately
    on an exact match; the target can lie outside every achievable sum.
Edge cases:
  - Exactly three numbers
  - Target far outside the achievable range
  - Exact match exists
  - Duplicates and negatives

Time O(n²), space O(1).
"""

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        # Sorting lets a two-pointer sweep find the best pair for each fixed first
        # element, instead of trying every pair.
        nums.sort()
        best = nums[0] + nums[1] + nums[2]
        for i in range(len(nums) - 2):
            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if abs(total - target) < abs(best - target):
                    best = total
                if total == target:
                    return total  # cannot get closer than exact
                # Too small: only a larger left value can raise the sum; too large:
                # only a smaller right value can lower it.
                if total < target:
                    left += 1
                else:
                    right -= 1
        return best
