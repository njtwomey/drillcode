"""Sum of Two Integers (#371, medium)

Approach: Loop: carry = (a & b) << 1; a = a ^ b; b = carry; until b is 0.
Tricks: XOR is the sum without carry and AND-shift is the carry; mask to 32 bits in
    Python.
Edge cases:
  - Negatives (two's complement handling in Python)
  - a + b = 0

Time O(1), space O(1).
"""


class Solution:
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        a &= mask
        b &= mask
        while b:
            a, b = (a ^ b) & mask, ((a & b) << 1) & mask
        return a if a <= 0x7FFFFFFF else ~(a ^ mask)
