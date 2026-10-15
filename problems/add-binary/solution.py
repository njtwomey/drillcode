"""Add Binary (#67, easy)

Approach: Add digit by digit from the right of both strings with a carry, then reverse
    the collected bits.
Tricks: Loop while either string has digits or a carry remains so unequal lengths and
    the final carry are handled together.
Edge cases:
  - Strings of different lengths
  - Carry out of the top digit
  - "0" plus "0"

Time O(max(m, n)), space O(max(m, n)).
"""

class Solution:
    def addBinary(self, a: str, b: str) -> str:
        # Schoolbook addition from the least significant digit. Looping while either
        # string has digits or a carry remains handles unequal lengths and the final
        # carry out of the top in one place.
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        digits = []
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += int(a[i])
                i -= 1
            if j >= 0:
                total += int(b[j])
                j -= 1
            digits.append(str(total % 2))  # the bit written at this position
            carry = total // 2  # 0 or 1 passed to the next position
        # Bits were produced least significant first; "0" + "0" yields no digits.
        return "".join(reversed(digits)) or "0"
