"""Longest Palindromic Substring (#5, medium)

Approach: Expand around each centre, both odd (i, i) and even (i, i + 1).
Tricks: Two centre types per index; Manacher's exists but is rarely expected.
Edge cases:
  - Single character
  - Whole string is a palindrome
  - All characters equal

Time O(n²), space O(1).
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        best_lo, best_hi = 0, 0

        def expand(lo, hi):
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1
                hi += 1
            return lo + 1, hi - 1

        for i in range(len(s)):
            for lo, hi in (expand(i, i), expand(i, i + 1)):
                if hi - lo > best_hi - best_lo:
                    best_lo, best_hi = lo, hi
        return s[best_lo:best_hi + 1]
