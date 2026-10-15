"""Capacity To Ship Packages Within D Days (#1011, medium)

Approach: Binary search the capacity between max(weights) and sum(weights); a capacity
    works if greedy daily loading takes at most days.
Tricks: The lower bound must be the heaviest package, otherwise the greedy check
    silently mishandles a package larger than the capacity.
Edge cases:
  - days = 1 (answer is the total weight)
  - days = n (answer is the heaviest package)
  - Single package
  - Packages must stay in order

Time O(n log(sum)), space O(1).
"""

class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        # Days needed if the ship can carry at most cap per day. Packages must go in
        # order, so greedily load each day until the next one would overflow.
        def days_needed(cap: int) -> int:
            count, load = 1, 0
            for weight in weights:
                if load + weight > cap:
                    count += 1
                    load = 0
                load += weight
            return count

        # The ship must carry the heaviest package, and a capacity of sum(weights) always
        # finishes in one day. More capacity never needs more days, so binary search the
        # smallest capacity that fits within the limit.
        lo, hi = max(weights), sum(weights)
        while lo < hi:
            mid = (lo + hi) // 2
            if days_needed(mid) <= days:
                hi = mid  # mid is enough; try smaller
            else:
                lo = mid + 1
        return lo
