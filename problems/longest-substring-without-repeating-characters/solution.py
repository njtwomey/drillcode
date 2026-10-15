"""Sliding window with a map of char -> last index; on a repeat inside the window,
jump the left edge to just past the previous occurrence.

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
