"""Group Anagrams (#49, medium)

Approach: Map from a canonical key (sorted string or 26-count tuple) to its list of
    words.
Tricks: The count tuple avoids sorting, which matters for long words.
Edge cases:
  - Empty strings
  - Single word
  - Identical words

Time O(n · k), space O(n · k).
"""
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Key = letter-count signature, identical for all anagrams of each other.
        groups = defaultdict(list)
        for word in strs:
            # Counting is O(L) per word, versus O(L log L) for sorting the letters.
            counts = [0] * 26
            for ch in word:
                counts[ord(ch) - ord("a")] += 1
            # Lists can't be dict keys, so freeze the counts into a tuple.
            groups[tuple(counts)].append(word)
        return list(groups.values())
