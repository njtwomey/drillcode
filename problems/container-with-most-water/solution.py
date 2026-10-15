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
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            best = max(best, min(height[left], height[right]) * (right - left))
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return best
