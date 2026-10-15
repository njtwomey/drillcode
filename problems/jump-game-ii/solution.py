"""Jump Game II (#45, medium)

Approach: Greedy BFS layers; track the farthest reachable index and take a jump when the
    current layer ends.
Tricks: Stop the loop before the last index so no extra jump is counted at the end.
Edge cases:
  - Single element needs 0 jumps
  - First jump reaches the end
  - Zeros in the middle that must be jumped over

Time O(n), space O(1).
"""

class Solution:
    def jump(self, nums: List[int]) -> int:
        # Greedy over BFS layers. Every index in [start, end] is reachable with `jumps`
        # jumps. Exchange argument: among them, the one that reaches farthest dominates,
        # since any plan through another index can switch to it without needing more
        # jumps. So the next layer is simply (end, farthest].
        jumps = 0
        end = 0  # last index reachable with `jumps` jumps
        farthest = 0  # last index reachable with `jumps + 1` jumps
        # The final index needs no jump taken from it, so stop before it.
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == end:
                # Layer exhausted: one more jump is unavoidable to go beyond it.
                jumps += 1
                end = farthest
        return jumps
