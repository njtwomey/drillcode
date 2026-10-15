"""Candy (#135, hard)

Approach: Two passes, left to right then right to left, taking the larger candy count
    required by either neighbour.
Tricks: Equal ratings impose no constraint; take the max on the second pass so peaks
    keep both slopes.
Edge cases:
  - Equal neighbours
  - Strictly increasing or decreasing ratings
  - Peak between plateaus

Time O(n), space O(n).
"""

class Solution:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        # Every child needs one candy. Each neighbour rule is a one-directional
        # constraint, so we satisfy "higher than left" and "higher than right"
        # separately. Taking the max per child keeps both, and each pass sets the
        # smallest value its own rule allows, so the total is minimal.
        candies = [1] * n
        # Left to right: a child rated above the left neighbour gets one more than it.
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1
        # Right to left: same for the right neighbour, never lowering what the first
        # pass gave (a peak needs the larger of its two slopes).
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)
        return sum(candies)
