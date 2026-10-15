"""Kth Largest Element in an Array (#215, medium)

Approach: Min-heap of size k, or quickselect for average O(n).
Tricks: Quickselect partitions like quicksort but recurses into one side only.
Edge cases:
  - k = 1
  - k = n
  - Duplicates

Time O(n log k), space O(k).
"""
import heapq


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # Keep a min-heap of the k largest values seen so far. Its root is then the
        # smallest of those k, which is exactly the kth largest overall.
        heap = []
        for num in nums:
            if len(heap) < k:
                heapq.heappush(heap, num)
            # Heap is full: num only matters if it beats the current kth largest.
            elif num > heap[0]:
                heapq.heapreplace(heap, num)  # pop root and push num in one O(log k) step
        return heap[0]
