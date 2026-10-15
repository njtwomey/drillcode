"""Contains Duplicate (#217, easy)

Approach: Insert into a set, return true on the first repeat.
Tricks: Sorting gives O(n log n) with no extra memory if that is asked for.
Edge cases:
  - Empty or single element array

Time O(n), space O(n).
"""


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

    # Alternative: sort, then compare neighbours. O(n log n) time, O(1) extra space.
    def containsDuplicateSorted(self, nums: List[int]) -> bool:
        ordered = sorted(nums)
        return any(a == b for a, b in zip(ordered, ordered[1:]))
