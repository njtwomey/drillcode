"""Top K Frequent Elements (#347, medium)

Approach: Count frequencies; bucket by frequency and collect from the top, or use a heap
    of size k.
Tricks: Bucket sort is O(n) because frequencies are bounded by n.
Edge cases:
  - k equals the number of distinct values
  - All elements identical

Time O(n), space O(n).
"""
from collections import Counter


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        buckets = [[] for _ in range(len(nums) + 1)]
        for value, count in Counter(nums).items():
            buckets[count].append(value)
        result = []
        for count in range(len(nums), 0, -1):
            for value in buckets[count]:
                result.append(value)
                if len(result) == k:
                    return result
        return result
