"""ways(n) = ways(n-1) + ways(n-2), the Fibonacci recurrence, with two rolling variables.

Time O(n), space O(1).
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        prev, curr = 1, 1
        for _ in range(n - 1):
            prev, curr = curr, prev + curr
        return curr
