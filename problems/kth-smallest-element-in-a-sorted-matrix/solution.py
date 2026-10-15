"""Kth Smallest Element in a Sorted Matrix (#378, medium)

Approach: Min-heap of row heads: pop the smallest k - 1 times, pushing the next element
    of the popped row.
Tricks: Only the first k rows can matter; binary search on the value with a staircase
    count is the O(n log range) alternative.
Edge cases:
  - 1x1 matrix
  - Duplicate values each count toward k
  - k equals n squared (the maximum)

Time O(min(n, k) + k log min(n, k)), space O(min(n, k)).
"""

import heapq


class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        # Every row is sorted, so the smallest unseen value is always the head of
        # some row. Keep one head per row in a min-heap, pop the smallest k times,
        # and each time replace it with the next element of the same row.
        # (Alternative: binary search on the value, counting entries <= mid by
        # walking the staircase in O(n).)
        n = len(matrix)
        # Columns are sorted too, so only the first k rows can hold the k smallest.
        heap = [(matrix[r][0], r, 0) for r in range(min(n, k))]
        heapq.heapify(heap)
        for _ in range(k - 1):
            _, r, c = heapq.heappop(heap)
            if c + 1 < n:
                heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
        return heap[0][0]
