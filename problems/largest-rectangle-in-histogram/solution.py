"""Largest Rectangle in Histogram (#84, hard)

Approach: Keep a stack of indices with non-decreasing heights; when a shorter bar
    arrives, pop and measure each taller bar's rectangle.
Tricks: Append a height-0 sentinel so the final pops happen inside the loop, and take
    the left edge from the new stack top after popping.
Edge cases:
  - Single bar
  - All bars equal
  - Strictly increasing or decreasing heights
  - Zero-height bars splitting the histogram

Time O(n), space O(n).
"""

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        # The stack holds indices of bars with non-decreasing heights. A bar stays on it
        # until a shorter bar shows up, because that is the first moment we learn where
        # its rectangle ends on the right.
        # A trailing 0 bar forces every remaining bar to be popped and measured.
        bars = heights + [0]
        stack = []
        best = 0
        for i, bar in enumerate(bars):
            while stack and bars[stack[-1]] > bar:
                height = bars[stack.pop()]
                # After the pop, the new top is the nearest bar to the left that is not
                # taller than height (everything between was popped earlier because it
                # was taller). The rectangle spans from just after it up to i - 1.
                left = stack[-1] + 1 if stack else 0
                best = max(best, height * (i - left))
            stack.append(i)
        return best
