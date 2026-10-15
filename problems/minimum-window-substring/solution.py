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
        # need[ch] > 0 means the window still lacks that many of ch; <= 0 means it has
        # a surplus. `missing` counts required characters still lacking, so "window is
        # valid" is just missing == 0 (O(1) instead of comparing two counters).
        need = Counter(t)
        missing = len(t)
        best_start, best_len = 0, float("inf")
        left = 0
        for right, ch in enumerate(s):
            # Only count ch as progress if it was actually still needed.
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1  # goes negative for extras and for chars not in t
            if missing == 0:
                # Valid window. Shrink from the left while the leftmost char is surplus
                # (need < 0): removing it keeps the window valid and makes it shorter.
                while need[s[left]] < 0:
                    need[s[left]] += 1
                    left += 1
                if right - left + 1 < best_len:
                    best_start, best_len = left, right - left + 1
                # Deliberately break validity by dropping s[left] (needed, need == 0),
                # so the next loop iterations expand right to find a new valid window.
                need[s[left]] += 1
                missing += 1
                left += 1
        # left and right each only move forward, so the total work is O(m + n).
        return "" if best_len == float("inf") else s[best_start:best_start + best_len]
