"""Two pointers at both ends of the sorted array: move left up if the sum is too small, right down if too large.

Returns 1-indexed positions.
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
