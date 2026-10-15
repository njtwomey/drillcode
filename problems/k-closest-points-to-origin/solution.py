"""K Closest Points to Origin (#973, medium)

Approach: Max-heap of size k keyed on squared distance, or quickselect.
Tricks: Compare squared distances; the square root is unnecessary.
Edge cases:
  - k equals the number of points
  - Ties at equal distance

Time O(n log k), space O(k).
"""
import heapq


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Max-heap of size k via negated distances: the root is the worst of the k best,
        # so it is the one to evict. Cost O(n log k) rather than sorting in O(n log n).
        # Squared distance gives the same ordering as distance, avoiding sqrt.
        heap = []  # (-squared distance, index)
        for i, (x, y) in enumerate(points):
            heapq.heappush(heap, (-(x * x + y * y), i))
            # Over capacity: drop the farthest point.
            if len(heap) > k:
                heapq.heappop(heap)
        return [points[i] for _, i in heap]
