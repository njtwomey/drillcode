"""Two Sum II - Input Array Is Sorted (#167, medium)

Approach: Pointers at both ends; move left if the sum is too small, right if too large.
Tricks: Sorted input removes the need for a hash map and gives O(1) space.
Edge cases:
  - Answer uses the first and last elements
  - Output is 1-indexed

Time O(n), space O(1).
"""


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]
            if total < target:
                left += 1
            else:
                right -= 1
        return []
