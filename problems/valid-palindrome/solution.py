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
        # left and right close in from both ends. Everything outside them is already verified.
        left, right = 0, len(s) - 1
        while left < right:
            # Skip junk one side at a time; each step moves a pointer, so O(n) total.
            if not s[left].isalnum():
                left += 1
            elif not s[right].isalnum():
                right -= 1
            else:
                # Both point at real characters: they must match ignoring case.
                if s[left].lower() != s[right].lower():
                    return False
                left += 1
                right -= 1
        return True
