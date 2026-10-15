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
        for center in range(2 * n - 1):
            left = center // 2
            right = left + center % 2
            while left >= 0 and right < n and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
        return count
