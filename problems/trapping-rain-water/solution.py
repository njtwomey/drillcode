"""Trapping Rain Water (#42, hard)

Approach: Two pointers with leftMax and rightMax; advance the side with the smaller max
    and add its max minus the height.
Tricks: Water at i is min(leftMax, rightMax) - height[i]; the two-pointer form avoids
    the two prefix arrays.
Edge cases:
  - Fewer than three bars (0)
  - Monotonic heights (0)
  - All equal

Time O(n), space O(1).
"""


class Solution:
    def trap(self, height: List[int]) -> int:
        # Water above a bar = min(tallest bar to its left, tallest to its right) - bar.
        # We track running maxes from both ends instead of building prefix arrays.
        left, right = 0, len(height) - 1
        left_max = right_max = 0
        total = 0
        while left < right:
            # The smaller end decides: if height[left] < height[right], then some bar
            # on the right is at least as tall as anything on the left, so the water
            # at `left` depends only on left_max. Symmetric for the else branch.
            if height[left] < height[right]:
                left_max = max(left_max, height[left])
                total += left_max - height[left]  # 0 if this bar is the new max
                left += 1
            else:
                right_max = max(right_max, height[right])
                total += right_max - height[right]
                right -= 1
        return total
