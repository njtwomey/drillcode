"""Longest Consecutive Sequence (#128, medium)

Approach: Put values in a set; for each value with no predecessor in the set, count
    upward.
Tricks: Starting counts only from sequence starts (n - 1 absent) is what keeps it O(n).
Edge cases:
  - Empty array
  - Duplicates
  - Negative numbers

Time O(n), space O(n).
"""


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # A set gives O(1) membership and removes duplicates.
        values = set(nums)
        best = 0
        for num in values:
            # Only count from the start of a run. If num - 1 exists, this run is counted
            # from an earlier start. So each element is walked at most once overall,
            # which is why the inner while loop does not make this O(n^2).
            if num - 1 not in values:
                length = 1
                while num + length in values:
                    length += 1
                best = max(best, length)
        return best
