"""Count frequencies, bucket values by frequency (at most n), then collect from the highest bucket.

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
