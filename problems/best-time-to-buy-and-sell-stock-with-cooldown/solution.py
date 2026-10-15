"""Best Time to Buy and Sell Stock with Cooldown (#309, medium)

Approach: Three-state machine (held, sold, rest) updated once per day, where buying is
    only allowed from the rest state.
Tricks: Update sold from yesterday's held before changing held, and keep yesterday's
    sold to feed rest; a sale today blocks buying tomorrow.
Edge cases:
  - Single day or two days
  - Strictly decreasing prices (0)
  - Cooldown forcing a skipped trade

Time O(n), space O(1).
"""

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # State machine, one state per "what am I doing at the end of today":
        #   held = best profit while holding a share
        #   sold = best profit on a day we just sold (tomorrow is forced cooldown)
        #   rest = best profit while holding nothing and free to buy
        # Transitions per price:
        #   held <- stay held, or buy from rest (never from sold: that is the cooldown)
        #   sold <- sell the share held yesterday
        #   rest <- stay resting, or arrive from yesterday's sale (cooldown day ends)
        # Base case before day 0: nothing held (impossible, so -infinity) and no profit.
        held = float("-inf")
        sold = float("-inf")
        rest = 0

        for price in prices:
            prev_sold = sold
            # Update order matters: sold reads yesterday's held, held reads yesterday's
            # rest, and rest reads yesterday's sold. Compute in that order, keeping
            # prev_sold aside.
            sold = held + price
            held = max(held, rest - price)
            rest = max(rest, prev_sold)

        # Ending while still holding is never better than having sold or rested.
        return max(sold, rest, 0)
