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
        # Inclusive bounds of the best palindrome so far; a single char is always one.
        best_lo, best_hi = 0, 0

        # Grow outward while the ends match. Stops on the first mismatch or boundary, so
        # left and right are one step past the palindrome; undo that on return.
        def expand(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return left + 1, right - 1

        # Every palindrome has a centre: a character (odd length) or a gap between two
        # (even length). Trying both at each index covers all 2n - 1 centres.
        for i in range(len(s)):
            for left, right in (expand(i, i), expand(i, i + 1)):
                # Compare spans, not lengths; the off-by-one cancels on both sides.
                if right - left > best_hi - best_lo:
                    best_lo, best_hi = left, right
        return s[best_lo:best_hi + 1]
