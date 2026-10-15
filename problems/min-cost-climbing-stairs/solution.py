"""Min Cost Climbing Stairs (#746, easy)

Approach: Roll two states, the cheapest cost of a path ending on each of the last two
    steps, and take the min of them at the end.
Tricks: The top is reachable from either of the last two steps, so the answer is
    min(prev, curr), not just the last state.
Edge cases:
  - Exactly two steps
  - Very expensive last step that should be skipped
  - All costs zero

Time O(n), space O(1).
"""

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # State: prev and curr are the cheapest total cost of a path that ends by
        # standing on step i-1 and step i, with that step's own cost already paid.
        # Starting on step 0 or 1 is allowed, so each begins at its own cost.
        prev, curr = cost[0], cost[1]
        for step_cost in cost[2:]:
            # Step i is reached from step i-1 (one step) or i-2 (two steps).
            prev, curr = curr, step_cost + min(prev, curr)
        # The top sits one past the last step and is reachable from either of the last
        # two, so the answer is the cheaper of them, not just the last state.
        return min(prev, curr)
