"""Min-heap of size k; after scanning, its root is the kth largest.

Quickselect would give average O(n), but the heap is simpler and deterministic.
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
