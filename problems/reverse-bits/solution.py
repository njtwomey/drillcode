"""Loop exactly 32 times: shift the result left and OR in the lowest bit of n, then shift n right.

Time O(1), space O(1).
"""


class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result
