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
        # Invariant: if an answer exists, it lies within [left, right]. Sortedness is
        # what lets us discard one end per step instead of trying every pair.
        left, right = 0, len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]  # problem wants 1-indexed positions
            if total < target:
                # Even paired with the largest remaining value, numbers[left] is too
                # small, so it can't be part of any answer. Drop it.
                left += 1
            else:
                # Even paired with the smallest remaining value, numbers[right] is
                # too big. Drop it.
                right -= 1
        return []  # unreachable: the problem guarantees exactly one solution
