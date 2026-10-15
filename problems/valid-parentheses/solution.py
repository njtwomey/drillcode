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
        # Keyed by closer so `ch in pairs` also tells us whether ch is a closer.
        pairs = {")": "(", "]": "[", "}": "{"}
        # The most recent unclosed opener must be the first one closed (LIFO).
        stack = []
        for ch in s:
            if ch in pairs:
                # A closer with an empty stack has nothing to match; otherwise the top
                # opener must be its partner.
                if not stack or stack.pop() != pairs[ch]:
                    return False
            else:
                stack.append(ch)
        # Leftover openers were never closed.
        return not stack
