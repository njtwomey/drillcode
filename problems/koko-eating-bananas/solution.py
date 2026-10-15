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
        lo, hi = 1, max(piles)
        while lo < hi:
            mid = (lo + hi) // 2
            hours = sum((pile + mid - 1) // mid for pile in piles)
            if hours <= h:
                hi = mid
            else:
                lo = mid + 1
        return lo
