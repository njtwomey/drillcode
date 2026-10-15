"""Max-heap of size k keyed on squared distance (negated for heapq); the sqrt is unnecessary.

Time O(n log k), space O(k).
"""
import heapq


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []  # (-squared distance, index)
        for i, (x, y) in enumerate(points):
            heapq.heappush(heap, (-(x * x + y * y), i))
            if len(heap) > k:
                heapq.heappop(heap)
        return [points[i] for _, i in heap]
