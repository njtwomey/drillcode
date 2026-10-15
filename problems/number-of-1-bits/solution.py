"""n &= n - 1 clears the lowest set bit, so count iterations until n is zero.

Time O(k) for k set bits, space O(1).
"""


class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1
            count += 1
        return count
