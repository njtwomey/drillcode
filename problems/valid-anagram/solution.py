"""Valid Anagram (#242, easy)

Approach: Compare letter counts with a 26-element array or a map.
Tricks: Compare lengths first for a fast reject.
Edge cases:
  - Different lengths
  - Unicode input if the follow-up asks

Time O(n), space O(1).
"""
from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Different lengths can never match; skip the counting.
        if len(s) != len(t):
            return False
        # Anagrams have identical letter frequencies. Counting is O(n) vs O(n log n)
        # for sorting both strings; the alphabet is fixed, so the map is O(1) space.
        return Counter(s) == Counter(t)
