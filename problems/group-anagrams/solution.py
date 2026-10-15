"""Group words in a dict keyed by a 26-slot letter-count tuple (no sorting needed).

Time O(n * k), space O(n * k).
"""
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for word in strs:
            counts = [0] * 26
            for ch in word:
                counts[ord(ch) - ord("a")] += 1
            groups[tuple(counts)].append(word)
        return list(groups.values())
