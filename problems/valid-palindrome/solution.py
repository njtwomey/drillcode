"""Valid Palindrome (#125, easy)

Approach: Two pointers moving inward, skipping non-alphanumeric characters, comparing
    case-insensitively.
Tricks: Skip inside the loop rather than building a filtered copy, if space matters.
Edge cases:
  - Empty string and all-punctuation strings count as palindromes

Time O(n), space O(1).
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        # i and j close in from both ends. Everything outside them is already verified.
        i, j = 0, len(s) - 1
        while i < j:
            # Skip junk one side at a time; each step moves a pointer, so O(n) total.
            if not s[i].isalnum():
                i += 1
            elif not s[j].isalnum():
                j -= 1
            else:
                # Both point at real characters: they must match ignoring case.
                if s[i].lower() != s[j].lower():
                    return False
                i += 1
                j -= 1
        return True
