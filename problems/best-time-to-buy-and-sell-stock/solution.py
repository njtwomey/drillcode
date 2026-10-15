"""One pass tracking the lowest price seen so far and the best profit selling today.

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
