"""Greedy: track the furthest reachable index; fail if the current index is beyond it.

Time O(n), space O(1).
"""


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        furthest = 0
        for i, jump in enumerate(nums):
            if i > furthest:
                return False
            furthest = max(furthest, i + jump)
        return True
