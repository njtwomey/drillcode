"""Last Stone Weight (#1046, easy)

Approach: Max-heap via negated values; repeatedly smash the two heaviest and push back
    any remainder.
Tricks: heapq is a min-heap, so negate weights; an empty heap at the end means the
    answer is 0.
Edge cases:
  - Single stone
  - Two equal stones
  - Everything cancels out

Time O(n log n), space O(n).
"""

import heapq


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        # heapq is a min-heap, so store negated weights to pop the heaviest first.
        heap = [-stone for stone in stones]
        heapq.heapify(heap)
        while len(heap) > 1:
            first = -heapq.heappop(heap)   # heaviest
            second = -heapq.heappop(heap)  # next heaviest
            # Equal stones destroy each other; otherwise the remainder goes back.
            if first != second:
                heapq.heappush(heap, -(first - second))
        return -heap[0] if heap else 0
