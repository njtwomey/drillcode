"""Koko Eating Bananas (#875, medium)

Approach: Binary search the speed in [1, max(piles)]; feasible if sum of ceil(pile /
    speed) <= h.
Tricks: Feasibility is monotonic in speed, so search the answer space rather than the
    input.
Edge cases:
  - h equals the number of piles (answer is the largest pile)
  - Single pile

Time O(n log m), space O(1).
"""


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # Answer lies in [1, max(piles)]: max(piles) always works (one pile per hour,
        # given h >= len(piles)), and speed 0 is meaningless.
        lo, hi = 1, max(piles)
        while lo < hi:
            # Invariant: the answer is in [lo, hi]. Faster speed never hurts, so
            # "feasible" flips from False to True exactly once as speed grows.
            mid = (lo + hi) // 2
            # (pile + mid - 1) // mid is integer ceil(pile / mid): a partial pile
            # still costs a whole hour.
            hours = sum((pile + mid - 1) // mid for pile in piles)
            if hours <= h:
                hi = mid  # mid works, but a slower speed might too; keep it
            else:
                lo = mid + 1  # mid is too slow, so everything <= mid is too
        return lo  # lo == hi: the smallest feasible speed
