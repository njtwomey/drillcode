"""Reject on length mismatch, then compare letter counts with Counter.

Time O(n), space O(1) for a fixed alphabet. Counter also handles Unicode input.
"""
from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)
