"""Open the Lock (#752, medium)

Approach: BFS over the 10,000 wheel states from "0000", seeding the visited set with the
    dead ends and counting turns by level.
Tricks: Dead ends are just pre-visited nodes; check for "0000" among them first and wrap
    digits with modulo 10.
Edge cases:
  - "0000" is a dead end
  - Target is "0000"
  - Target walled in by dead ends
  - Wrap-around from 0 to 9

Time O(10^4 * 8), space O(10^4).
"""

from collections import deque


class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        # Treat the 10,000 wheel states as graph nodes; one turn of one wheel is an
        # edge. Dead ends are simply pre-visited nodes, so BFS never enters them.
        seen = set(deadends)
        if "0000" in seen:
            return -1  # the lock is jammed before the first turn
        seen.add("0000")
        queue = deque([("0000", 0)])
        while queue:
            curr, turns = queue.popleft()
            if curr == target:
                return turns
            for i in range(4):
                digit = int(curr[i])
                # Each wheel turns up or down, wrapping 9 -> 0 and 0 -> 9 via modulo.
                for step in (1, -1):
                    nxt = curr[:i] + str((digit + step) % 10) + curr[i + 1:]
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append((nxt, turns + 1))
        return -1
