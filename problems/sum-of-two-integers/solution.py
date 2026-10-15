"""XOR gives the sum without carry; (a & b) << 1 is the carry. Repeat until no carry remains.

Python ints are unbounded, so mask to 32 bits and sign-convert the result.
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
