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
        # Invariant: lowest is the cheapest price seen so far (the best day to have bought).
        lowest = float("inf")
        best = 0
        for price in prices:
            # Update the buy price first so a same-day sale gives profit 0, never negative.
            lowest = min(lowest, price)
            # Best sale today is today's price minus the cheapest earlier price.
            best = max(best, price - lowest)
        return best
