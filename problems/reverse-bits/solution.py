"""Reverse Bits (#190, easy)

Approach: Loop 32 times: shift the result left, OR in n's lowest bit, shift n right.
Tricks: The loop must run exactly 32 times, not until n is zero.
Edge cases:
  - n = 0
  - Only the top bit set

Time O(1), space O(1).
"""


class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result
