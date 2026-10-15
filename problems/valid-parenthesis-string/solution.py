"""Valid Parenthesis String (#678, medium)

Approach: Track the range [lo, hi] of possible open-parenthesis counts in one pass and
    require 0 to be reachable at the end.
Tricks: Clamp lo at 0 because a negative count just means a star should have been empty;
    return False the moment hi goes below 0.
Edge cases:
  - Star before an open parenthesis ("*(")
  - Closing parenthesis first
  - Only stars
  - Single star

Time O(n), space O(1).
"""

class Solution:
    def checkValidString(self, s: str) -> bool:
        # Instead of guessing what each '*' is, track the whole range [lo, hi] of open
        # parenthesis counts that some choice of stars could have produced so far.
        lo = hi = 0
        for ch in s:
            if ch == '(':
                lo += 1
                hi += 1
            elif ch == ')':
                lo -= 1
                hi -= 1
            else:  # '*' is ')' (lo - 1), empty (no change) or '(' (hi + 1)
                lo -= 1
                hi += 1
            # Even with every star as '(' there are too few openers: a ')' is unmatched
            # in every interpretation, so no later character can repair it.
            if hi < 0:
                return False
            # A negative open count is not a real state, it just means the star we spent
            # as ')' should have been empty instead. Clamp so lo stays the smallest
            # achievable non-negative count; without it "*(" would wrongly pass.
            lo = max(lo, 0)
        # Valid only if zero open parentheses is among the achievable counts.
        return lo == 0
