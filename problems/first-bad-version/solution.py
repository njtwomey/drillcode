"""First Bad Version (#278, easy)

Approach: Binary search for the first index where isBad is true.
Tricks: Set hi = mid, not mid - 1, when mid is bad, so the answer is never discarded.
Edge cases:
  - n = 1
  - First version bad
  - Last version bad

Time O(log n), space O(1).
"""


# The isBadVersion API is already defined by LeetCode.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        lo, hi = 1, n
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if isBadVersion(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
