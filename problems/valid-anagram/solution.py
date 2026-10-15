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
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)
