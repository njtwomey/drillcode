"""Sqrt(x) (#69, easy)

Approach: Binary search the largest r in [0, x] with r * r <= x, rounding mid up so the
    loop always shrinks.
Tricks: Use the upper midpoint when the true branch sets lo = mid, otherwise lo and hi =
    lo + 1 never converge.
Edge cases:
  - x = 0 and x = 1
  - Non-perfect squares round down
  - x = 2^31 - 1 (mid * mid is large, fine in Python but overflows in fixed-width
    languages)

Time O(log x), space O(1).
"""

class Solution:
    def mySqrt(self, x: int) -> int:
        # Find the largest r with r * r <= x. The predicate is true for small r and false
        # for large r, so binary search the boundary. The answer is never above x.
        lo, hi = 0, x
        while lo < hi:
            # Round mid up: with lo = mid below, rounding down would loop forever
            # once hi == lo + 1.
            mid = (lo + hi + 1) // 2
            if mid * mid <= x:
                lo = mid  # mid is a valid root, but a larger one may exist
            else:
                hi = mid - 1  # mid is too big, and so is everything above it
        return lo
