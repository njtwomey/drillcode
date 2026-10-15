"""Jump Game (#55, medium)

Approach: Track the furthest reachable index; fail if the current index is beyond it.
Tricks: Greedy is simpler than DP here; the reverse version tracks the leftmost index
    that can reach the end.
Edge cases:
  - Single element (true)
  - Zero before the end that can be jumped over
  - Zero at the last index

Time O(n), space O(1).
"""


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        # furthest = farthest index reachable using the positions seen so far (greedy).
        furthest = 0
        for i, jump in enumerate(nums):
            # A gap: no earlier jump reaches i, and nothing later can jump back over it.
            if i > furthest:
                return False
            furthest = max(furthest, i + jump)
        return True
