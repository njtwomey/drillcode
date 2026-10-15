"""Binary search for the first index where isBadVersion is true.

When mid is bad keep it (hi = mid) so the answer is never discarded.
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
