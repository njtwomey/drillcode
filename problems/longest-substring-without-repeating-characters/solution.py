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
        # seen[c] = most recent index of c. Window is s[left..right] with no repeats.
        seen = {}
        left = 0
        best = 0
        for right, c in enumerate(s):
            # Jump left past the previous copy of c instead of shrinking step by step.
            # max() matters: seen[c] may sit left of the window already (stale entry),
            # and moving left backwards would readmit duplicates.
            if c in seen:
                left = max(left, seen[c] + 1)
            seen[c] = right
            best = max(best, right - left + 1)
        return best
