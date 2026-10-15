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
        heap = []
        for num in nums:
            if len(heap) < k:
                heapq.heappush(heap, num)
            elif num > heap[0]:
                heapq.heapreplace(heap, num)
        return heap[0]
