"""Top K Frequent Words (#692, medium)

Approach: Count words, then take the k smallest by key (-count, word) with
    heapq.nsmallest.
Tricks: Negating the count lets one ascending key express frequency descending then
    alphabetical order.
Edge cases:
  - Ties broken lexicographically
  - k equals the number of distinct words
  - One word

Time O(n log k), space O(n).
"""

import heapq
from collections import Counter


class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        count = Counter(words)
        # Order by higher frequency first, then alphabetically for ties. Negating the
        # count lets one ascending key express both rules. nsmallest keeps only k items
        # in a heap, so this is O(n log k) rather than a full sort.
        return heapq.nsmallest(k, count, key=lambda word: (-count[word], word))
