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
        i, j = 0, len(s) - 1
        while i < j:
            if not s[i].isalnum():
                i += 1
            elif not s[j].isalnum():
                j -= 1
            else:
                if s[i].lower() != s[j].lower():
                    return False
                i += 1
                j -= 1
        return True
