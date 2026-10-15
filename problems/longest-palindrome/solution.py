"""Longest Palindrome (#409, easy)

Approach: Count each character, add every complete pair, and add one more if any
    character has a leftover odd count.
Tricks: Only one odd leftover can be the centre, so add 1 once rather than per odd
    count; matching is case-sensitive.
Edge cases:
  - A single character
  - All characters in pairs
  - Several odd counts
  - Mixed case such as Aa

Time O(n), space O(1).
"""

from collections import Counter

class Solution:
    def longestPalindrome(self, s: str) -> int:
        # We may reorder letters freely, so a palindrome is built from pairs placed
        # symmetrically, plus at most one unpaired letter in the centre.
        count = Counter(s)  # case-sensitive: 'a' and 'A' are different letters
        result = 0
        has_odd = False
        for c in count.values():
            result += c // 2 * 2  # every complete pair of a letter can be used
            if c % 2:
                has_odd = True  # a leftover single letter could sit in the middle
        return result + 1 if has_odd else result
