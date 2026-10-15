"""Number of 1 Bits (#191, easy)

Approach: Loop n &= n - 1, counting iterations.
Tricks: n & (n - 1) clears the lowest set bit, so the loop runs once per set bit.
Edge cases:
  - n = 0
  - All 32 bits set (treat as unsigned)

Time O(k), space O(1).
"""


class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        # n - 1 flips the lowest set bit to 0 and every zero below it to 1, so
        # n & (n - 1) wipes exactly that one bit. Each pass removes one set bit,
        # so we loop once per 1 bit instead of 32 times.
        while n:
            n &= n - 1
            count += 1
        return count
