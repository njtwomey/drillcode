"""Max-heap (negated) for the lower half, min-heap for the upper half.
Push to the lower heap, move its top to the upper, then rebalance so the lower
heap is never smaller than the upper and exceeds it by at most one.

Time O(log n) add, O(1) median, space O(n).
"""
import heapq


class MedianFinder:
    def __init__(self):
        self.low = []   # max-heap via negation
        self.high = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
