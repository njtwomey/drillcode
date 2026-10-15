"""Palindromic Substrings (#647, medium)

Approach: Expand around each of the 2n - 1 centres, counting every successful expansion.
Tricks: Same technique as Longest Palindromic Substring, counting instead of tracking
    the max.
Edge cases:
  - Single character
  - All characters equal (n(n+1)/2)

Time O(n²), space O(1).
"""


class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        count = 0
        # A palindrome mirrors around its centre. There are 2n - 1 centres: n on
        # characters (odd length) and n - 1 between characters (even length).
        for center in range(2 * n - 1):
            left = center // 2
            right = left + center % 2  # even centres start with right = left + 1
            # Invariant: s[left+1..right-1] is already a palindrome, so each match of
            # the outer pair is exactly one more palindromic substring.
            while left >= 0 and right < n and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
        # O(n^2) worst case (all equal chars), but O(1) extra space.
        return count
