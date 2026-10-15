"""Best Time to Buy and Sell Stock (#121, easy)

Approach: One pass tracking the minimum price so far and the best profit.
Tricks: Profit is always price[i] minus an earlier minimum, so no pair enumeration is
    needed.
Edge cases:
  - Strictly decreasing prices (answer 0)
  - Single price

Time O(n), space O(1).
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        lowest = float("inf")
        best = 0
        for price in prices:
            lowest = min(lowest, price)
            best = max(best, price - lowest)
        return best
