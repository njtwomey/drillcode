"""Longest Substring Without Repeating Characters (#3, medium)

Approach: Window with a map of char → last index; jump the left edge past the previous
    occurrence.
Tricks: Set left = max(left, last[c] + 1) rather than shrinking one step at a time.
Edge cases:
  - Empty string
  - All identical characters
  - All distinct

Time O(n), space O(min(n, alphabet)).
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = {}
        left = 0
        best = 0
        for right, c in enumerate(s):
            if c in last:
                left = max(left, last[c] + 1)
            last[c] = right
            best = max(best, right - left + 1)
        return best
