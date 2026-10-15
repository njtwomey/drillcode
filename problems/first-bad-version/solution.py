"""First Bad Version (#278, easy)

Approach: Binary search for the first index where isBad is true.
Tricks: Set hi = mid, not mid - 1, when mid is bad, so the answer is never discarded.
Edge cases:
  - n = 1
  - First version bad
  - Last version bad

Time O(log n), space O(1).
"""

# Judge notes:
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:


class Solution:
    def firstBadVersion(self, n: int) -> int:
        # Invariant: the first bad version is always within [lo, hi].
        lo, hi = 1, n
        while lo < hi:  # Stop when one candidate is left; it must be the answer.
            mid = lo + (hi - lo) // 2
            if isBadVersion(mid):
                # mid might itself be the first bad one, so keep it in range.
                hi = mid
            else:
                # mid is good, so everything up to and including it is good too.
                lo = mid + 1
        return lo
