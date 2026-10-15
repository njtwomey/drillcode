"""Contains Duplicate (#217, easy)

Approach: Insert into a set, return true on the first repeat.
Tricks: Sorting gives O(n log n) with no extra memory if that is asked for.
Edge cases:
  - Empty or single element array

Time O(n), space O(n).
"""


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        # A set gives O(1) average lookups, so one pass replaces comparing every pair (O(n^2)).
        seen = set()
        for num in nums:
            if num in seen:  # Seen before, so this value appears at least twice.
                return True
            seen.add(num)
        return False

    # Alternative: sort, then compare neighbours. O(n log n) time, O(1) extra space.
    def containsDuplicateSorted(self, nums: List[int]) -> bool:
        # After sorting, equal values must sit next to each other, so only neighbours matter.
        ordered = sorted(nums)
        return any(a == b for a, b in zip(ordered, ordered[1:]))
