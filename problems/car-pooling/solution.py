"""Car Pooling (#1094, medium)

Approach: Difference array over stops, then a running sum checked against capacity.
Tricks: Passengers leave at `to` before others board there, so each trip covers the
    half-open range [from, to).
Edge cases:
  - Load exactly equal to capacity is allowed
  - Drop off and pick up at the same stop
  - Trips given out of order

Time O(n + m), space O(m).
"""

class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        # Difference array over stops: change[x] is the net passengers boarding at x.
        # Passengers leave at `to` before anyone boards there, so a trip occupies the
        # half-open range [from, to): add at `from`, subtract at `to`.
        last_stop = max(to for _, _, to in trips)
        change = [0] * (last_stop + 1)
        for passengers, start, to in trips:
            change[start] += passengers
            change[to] -= passengers
        # A running sum of the changes is the load while driving past each stop; the
        # trip is feasible iff the load never exceeds capacity.
        load = 0
        for delta in change:
            load += delta
            if load > capacity:
                return False
        return True
