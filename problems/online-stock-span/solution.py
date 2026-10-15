"""Online Stock Span (#901, medium)

Approach: Keep a stack of (price, span) with decreasing prices; pop entries <= today's
    price and add their spans to today's.
Tricks: Store the accumulated span with each entry so popped runs are absorbed in O(1)
    instead of re-walked.
Edge cases:
  - Equal prices (span includes them)
  - Strictly decreasing prices (always 1)
  - A new high that swallows the whole history

Time O(1) amortised per call, space O(n).
"""

class StockSpanner:
    def __init__(self):
        # Stack of (price, span) with strictly decreasing prices. Each entry stands for a
        # run of consecutive days whose prices are all <= that entry's price.
        self.stack = []

    def next(self, price: int) -> int:
        span = 1  # today always counts
        # Every earlier day covered by a popped entry also has a price <= today's, so
        # absorb its whole span at once instead of walking those days one by one.
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span
