"""Find K Pairs with Smallest Sums (#373, medium)

Approach: Seed a min-heap with (nums1[i] + nums2[0], i, 0) for the first k rows, then
    pop and push the successor (i, j + 1).
Tricks: Treat each nums1 value as a sorted row and merge the rows lazily; rows beyond
    the first k can never matter.
Edge cases:
  - k larger than the number of pairs
  - Duplicate values and tied sums
  - Negative numbers

Time O(k log k), space O(k).
"""

import heapq


class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2:
            return []
        # Both arrays are sorted, so for a fixed i the sums nums1[i] + nums2[j] grow with j.
        # Think of one sorted list per i and merge them lazily: the heap holds just the
        # current front of each list, as (sum, i, j).
        # Only the first k values of nums1 can matter: pair (i, 0) is beaten by
        # (0, 0) .. (i - 1, 0), so any row past k never reaches the top k.
        heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
        heapq.heapify(heap)
        result = []
        while heap and len(result) < k:
            _, i, j = heapq.heappop(heap)
            result.append([nums1[i], nums2[j]])
            # The next candidate from row i is its successor in nums2.
            if j + 1 < len(nums2):
                heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
        return result
