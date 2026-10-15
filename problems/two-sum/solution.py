"""Two Sum (#1, easy)

Approach: One pass with a map of value → index, checking for the complement before
    inserting.
Tricks: Check before inserting, or an element can pair with itself.
Edge cases:
  - Duplicates such as [3, 3] with target 6
  - Negatives
  - Zero

Time O(n), space O(n).
"""


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # seen maps value -> index for elements strictly before the current one.
        seen = {}
        for i, num in enumerate(nums):
            # If the partner appeared earlier we are done. Checking before inserting
            # stops an element pairing with itself, yet [3, 3] still works.
            if target - num in seen:
                return [seen[target - num], i]
            seen[num] = i
        return []  # unreachable: the problem guarantees one answer
