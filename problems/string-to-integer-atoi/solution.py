"""String to Integer (atoi) (#8, medium)

Approach: Single left-to-right scan in phases: skip spaces, read one optional sign,
    accumulate digits, then clamp to the 32-bit range.
Tricks: Compare characters to '0'..'9' instead of using isdigit, stop accumulating once
    past 2**31, and let a second sign or no digits fall out as 0.
Edge cases:
  - Empty, all-space and sign-only strings
  - Leading zeros and letters after the digits
  - Overflow clamping to 2**31 - 1 and -2**31
  - Two signs or a space after the sign

Time O(n), space O(1).
"""

class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX, INT_MIN = 2**31 - 1, -(2**31)
        i, n = 0, len(s)
        # Phase 1: skip leading spaces (only the space character counts).
        while i < n and s[i] == " ":
            i += 1
        # Phase 2: at most one sign. A second sign is not a digit, so phase 3 reads
        # nothing and the answer is 0 ("+-12" gives 0).
        sign = 1
        if i < n and s[i] in "+-":
            if s[i] == "-":
                sign = -1
            i += 1
        # Phase 3: read digits until the first non-digit. Compare against '0'..'9'
        # directly: str.isdigit() also accepts characters int() cannot parse.
        result = 0
        while i < n and "0" <= s[i] <= "9":
            result = result * 10 + (ord(s[i]) - 48)
            if result > INT_MAX + 1:  # already out of range either way, stop growing
                break
            i += 1
        # Phase 4: clamp. No digits at all leaves result at 0, which covers the empty,
        # all-space and sign-only strings.
        return max(INT_MIN, min(INT_MAX, sign * result))
