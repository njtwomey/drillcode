"""Gas Station (#134, medium)

Approach: One pass with a running tank; when it goes negative restart from the next
    station, and answer -1 if the total is negative.
Tricks: A failed stretch rules out every start inside it, and a non-negative total
    guarantees the last candidate works.
Edge cases:
  - Total gas less than total cost gives -1
  - Single station
  - Total exactly equal to total cost

Time O(n), space O(1).
"""

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # Invariant: `tank` is the fuel when arriving at station i having started at
        # `start`. If it goes negative at i, no station in [start, i] can be a valid
        # start either: each of them reaches i with at most as much fuel as `start` did
        # (they skip a prefix whose net gain was >= 0), so they fail too. Skip them all.
        total = 0  # net fuel over the whole circle
        tank = 0
        start = 0
        for i in range(len(gas)):
            gain = gas[i] - cost[i]
            total += gain
            tank += gain
            if tank < 0:
                start = i + 1
                tank = 0
        # If the circle as a whole has a deficit nothing works. Otherwise the surviving
        # candidate works: the part after `start` never dipped, and the part before it
        # has a deficit that the surplus after it covers.
        return start if total >= 0 else -1
