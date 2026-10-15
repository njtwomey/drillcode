"""4Sum (#18, medium)

Approach: Sort, fix the first two values with nested loops, then close in with left and
    right pointers on the rest.
Tricks: Skip repeated values at each level (i, j, then left and right after a hit) so no
    quadruplet is emitted twice.
Edge cases:
  - Fewer than four elements
  - All equal values
  - Duplicates producing repeated quadruplets
  - Sums beyond 32-bit range in other languages

Time O(n³), space O(1).
"""

class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        # Sort, fix the first two numbers with nested loops, and finish with two pointers.
        nums.sort()
        n = len(nums)
        result = []
        for i in range(n - 3):
            # Skip a repeated first value: it would rebuild the same quadruplets.
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            for j in range(i + 1, n - 2):
                # Same dedup for the second value, but only among choices after i.
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue
                left, right = j + 1, n - 1
                while left < right:
                    total = nums[i] + nums[j] + nums[left] + nums[right]
                    if total < target:
                        left += 1
                    elif total > target:
                        right -= 1
                    else:
                        result.append([nums[i], nums[j], nums[left], nums[right]])
                        left += 1
                        right -= 1
                        # Step past duplicates of the pair just used, or they repeat it.
                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
        return result
