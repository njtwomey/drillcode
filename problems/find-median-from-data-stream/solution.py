"""Find Median from Data Stream (#295, hard)

Approach: Max-heap for the lower half, min-heap for the upper; keep sizes within 1 of
    each other.
Tricks: Push to one heap then pop its top into the other to preserve ordering; Python
    needs negated values for a max-heap.
Edge cases:
  - Even count (average of the two tops)
  - Single element
  - Many duplicates

Time O(log n) add, O(1) median, space O(n).
"""

# Judge notes:
# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_1 = obj.findMedian()


import heapq


class MedianFinder:
    def __init__(self):
        # Invariants: every value in low <= every value in high, and
        # len(low) is len(high) or len(high) + 1. So the median is always at the tops.
        self.low = []   # max-heap via negation
        self.high = []  # min-heap

    def addNum(self, num: int) -> None:
        # Route through low then into high: this guarantees the largest of the lower
        # half moves up, so the ordering invariant holds whatever num is, without
        # comparing against the tops by hand.
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        # Rebalance so low keeps the extra element when the count is odd.
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])  # odd count: the middle is low's top
        return (-self.low[0] + self.high[0]) / 2  # even: average the two middles
