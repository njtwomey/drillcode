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
        # Python ints are unbounded, so negatives never wrap and the carry loop
        # would not terminate. Masking emulates 32-bit two's complement.
        mask = 0xFFFFFFFF
        a &= mask
        b &= mask
        # XOR adds each bit without carrying; AND shifted left is the carry bits.
        # Repeat, feeding the carry back in, until no carry is left. The carry moves
        # up at least one bit per round, so at most 32 rounds: O(1).
        while b:
            a, b = (a ^ b) & mask, ((a & b) << 1) & mask
        # If bit 31 is set the 32-bit result is negative. a ^ mask flips the low
        # 32 bits and ~ flips the rest, which gives Python's negative value.
        return a if a <= 0x7FFFFFFF else ~(a ^ mask)
