"""Valid Parentheses (#20, easy)

Approach: Push openers; on a closer, pop and check the pair matches.
Tricks: A map from closer to opener keeps the check to one line; the stack must be empty
    at the end.
Edge cases:
  - String starting with a closer
  - Unmatched openers left over
  - Empty string

Time O(n), space O(n).
"""


class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []
        for ch in s:
            if ch in pairs:
                if not stack or stack.pop() != pairs[ch]:
                    return False
            else:
                stack.append(ch)
        return not stack
