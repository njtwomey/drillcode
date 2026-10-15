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
        # Bucket sort by frequency: a value can occur at most len(nums) times, so
        # the buckets indexed 0..n cover every possible count. This beats sorting
        # (O(n log n)) because the keys are small bounded integers.
        buckets = [[] for _ in range(len(nums) + 1)]
        for value, count in Counter(nums).items():
            buckets[count].append(value)
        result = []
        # Walk from the highest frequency down; the first k values seen are the
        # answer. Total work is O(n): n buckets plus at most n values in them.
        for count in range(len(nums), 0, -1):
            for value in buckets[count]:
                result.append(value)
                if len(result) == k:
                    return result
        return result
