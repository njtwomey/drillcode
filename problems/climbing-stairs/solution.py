"""Climbing Stairs (#70, easy)

Approach: ways(n) = ways(n-1) + ways(n-2) with two rolling variables.
Tricks: It is Fibonacci; no array required.
Edge cases:
  - n = 1 and n = 2 base cases

Time O(n), space O(1).
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        # ways(0) = 1 (stay put) and ways(1) = 1; these seed the Fibonacci-style recurrence.
        prev, curr = 1, 1
        # curr already holds ways(1), so n - 1 steps reach ways(n). This also handles n = 1.
        for _ in range(n - 1):
            # Last step was 1 stair (from n-1) or 2 stairs (from n-2), so the counts add.
            prev, curr = curr, prev + curr
        return curr
