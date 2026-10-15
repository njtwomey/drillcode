"""Minimum Window Substring (#76, hard)

Approach: Expand right until every required count is met, then shrink left while still
    valid, recording the best.
Tricks: A counter of satisfied characters makes the validity check O(1).
Edge cases:
  - t longer than s
  - Repeated characters in t
  - The whole of s is the answer

Time O(m + n), space O(alphabet).
"""
from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(t) > len(s):
            return ""
        need = Counter(t)
        missing = len(t)
        best_start, best_len = 0, float("inf")
        left = 0
        for right, ch in enumerate(s):
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1
            if missing == 0:
                while need[s[left]] < 0:
                    need[s[left]] += 1
                    left += 1
                if right - left + 1 < best_len:
                    best_start, best_len = left, right - left + 1
                need[s[left]] += 1
                missing += 1
                left += 1
        return "" if best_len == float("inf") else s[best_start:best_start + best_len]
