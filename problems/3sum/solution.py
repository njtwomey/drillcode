"""3Sum (#15, medium)

Approach: Sort; for each i, run two pointers on the remainder looking for -nums[i].
Tricks: Skip duplicate values at i, left and right to avoid repeated triplets.
Edge cases:
  - All zeros
  - Fewer than three elements
  - No valid triplet

Time O(n²), space O(1).
"""


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Sorting enables two-pointer search and makes duplicates adjacent.
        nums.sort()
        n = len(nums)
        result = []
        # Fix the smallest element at i, then find pairs to its right summing to -nums[i].
        for i in range(n - 2):
            # Sorted, so if the smallest is positive, every sum is positive.
            if nums[i] > 0:
                break
            # Skip a repeated anchor value, or we would emit the same triplets again.
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            # Two pointers: O(n) per anchor, O(n^2) overall (the sort is dominated).
            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                # Too small: only moving left up can raise the sum. Too big: lower right.
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    # After recording, skip equal values on both sides so the same
                    # triplet is not recorded twice.
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
        return result
