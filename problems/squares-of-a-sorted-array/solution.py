"""Squares of a Sorted Array (#977, easy)

Approach: Two pointers at both ends; the larger absolute value gives the largest square,
    so fill the result from the back.
Tricks: Squares are largest at the ends of a sorted array with negatives, so build the
    output in descending order instead of sorting.
Edge cases:
  - All negative or all non-negative
  - Equal magnitudes with opposite signs
  - Single element

Time O(n), space O(n).
"""

class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        # The largest square is always at one of the two ends: negatives with the
        # biggest magnitude sit at the left, positives at the right. So fill the result
        # from the back, taking the larger square from either end each time.
        result = [0] * len(nums)
        left, right = 0, len(nums) - 1
        for i in range(len(nums) - 1, -1, -1):
            if abs(nums[left]) > abs(nums[right]):
                result[i] = nums[left] * nums[left]
                left += 1
            else:
                result[i] = nums[right] * nums[right]
                right -= 1
        return result
