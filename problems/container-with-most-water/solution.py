"""Container With Most Water (#11, medium)

Approach: Pointers at both ends; move the shorter side inward each step.
Tricks: Moving the taller side can never increase the area, which is what makes the
    greedy step safe.
Edge cases:
  - Two elements
  - All heights equal
  - Zero height at an end

Time O(n), space O(1).
"""


class Solution:
    def maxArea(self, height: List[int]) -> int:
        # Start at the widest container; every move inward loses width.
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            # Water level is capped by the shorter wall.
            best = max(best, min(height[left], height[right]) * (right - left))
            # Move the shorter wall. Any container that keeps it is capped by its height and
            # is narrower, so it can't beat what we just measured. Moving the taller wall
            # can't help for the same reason, so only the shorter side is worth giving up.
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return best
