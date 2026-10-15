"""Reverse Integer (#7, medium)

Approach: Peel digits off the absolute value with divmod and append them to the result,
    bailing out before an append would pass the 32-bit limit.
Tricks: Work on abs(x) because Python's // and % floor for negatives; the bound is 2**31
    - 1 for positives but 2**31 for negatives.
Edge cases:
  - Trailing zeros (120 becomes 21)
  - Overflow in either direction returns 0
  - Zero and negative inputs

Time O(log x), space O(1).
"""

class Solution:
    def reverse(self, x: int) -> int:
        # Work on the absolute value: in Python // and % round towards negative
        # infinity, so peeling digits from a negative number would go wrong.
        sign = -1 if x < 0 else 1
        x = abs(x)
        # The signed 32-bit range is asymmetric: [-2**31, 2**31 - 1].
        limit = 2**31 if sign < 0 else 2**31 - 1
        result = 0
        while x:
            x, digit = divmod(x, 10)
            # Check before appending, as a fixed-width language must: result * 10 + digit
            # exceeds limit exactly when result > (limit - digit) // 10.
            if result > (limit - digit) // 10:
                return 0
            result = result * 10 + digit
        return sign * result
