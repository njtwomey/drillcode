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
        seen = {}
        for i, num in enumerate(nums):
            if target - num in seen:
                return [seen[target - num], i]
            seen[num] = i
        return []
