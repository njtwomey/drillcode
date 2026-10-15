"""Climbing Stairs (#70, easy)

Approach: ways(n) = ways(n-1) + ways(n-2) with two rolling variables.
Tricks: It is Fibonacci; no array required.
Edge cases:
  - n = 1 and n = 2 base cases

Time O(n), space O(1).
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        prev, curr = 1, 1
        for _ in range(n - 1):
            prev, curr = curr, prev + curr
        return curr
