"""Reorganize String (#767, medium)

Approach: Reject if any letter exceeds ceil(n / 2), otherwise repeatedly pair the two
    most frequent letters using a max-heap.
Tricks: Pairing the two largest piles each round guarantees adjacent letters differ and
    nothing is left over except at most one single letter.
Edge cases:
  - Impossible when one letter exceeds ceil(n / 2)
  - Single character
  - Exactly at the bound

Time O(n), space O(1).
"""

import heapq
from collections import Counter


class Solution:
    def reorganizeString(self, s: str) -> str:
        count = Counter(s)
        # A letter with more than ceil(n / 2) copies cannot be kept apart, however
        # we arrange things. At or below that bound a valid arrangement always exists.
        if max(count.values()) > (len(s) + 1) // 2:
            return ""
        heap = [(-c, ch) for ch, c in count.items()]
        heapq.heapify(heap)
        result = []
        # Take the two most frequent letters each round and place them side by side.
        # They differ, so adjacent letters never match, and using the biggest piles
        # first keeps any one letter from being left over at the end.
        while len(heap) > 1:
            c1, ch1 = heapq.heappop(heap)
            c2, ch2 = heapq.heappop(heap)
            result.append(ch1)
            result.append(ch2)
            if c1 + 1 < 0:
                heapq.heappush(heap, (c1 + 1, ch1))
            if c2 + 1 < 0:
                heapq.heappush(heap, (c2 + 1, ch2))
        # At most one letter, with a single copy (guaranteed by the bound), remains.
        if heap:
            result.append(heap[0][1])
        return "".join(result)
