"""Kth Largest Element in a Stream (#703, easy)

Approach: Keep a min-heap of the k largest values seen; its root is the kth largest.
Tricks: Only values larger than the root can enter the top k, so replace the root with
    heapreplace and ignore the rest.
Edge cases:
  - Initial list shorter than k or empty
  - Duplicate values count separately
  - k equals 1

Time O(log k) per add, space O(k).
"""

import heapq


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        # Min-heap holding only the k largest values seen so far. Its root is the
        # smallest of those k, which is exactly the kth largest overall.
        self.heap = []
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif val > self.heap[0]:
            # Pop the old kth largest and push val in one step; a value no bigger
            # than the root can never be among the top k, so it is ignored.
            heapq.heapreplace(self.heap, val)
        return self.heap[0]
