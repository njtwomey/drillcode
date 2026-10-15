Implement `StockSpanner`, which receives a stream of daily stock prices one at a time and reports each day's span.

- `StockSpanner()`: create an empty tracker.
- `next(price)`: record today's `price` and return its span: the number of consecutive days, counting today and going backwards, whose price was less than or equal to today's.

Constraints:
- `1 <= price <= 10^5`
- Up to `10^4` calls to `next`
- Rescanning all earlier days on every call is too slow in the worst case; aim for amortised O(1) per call
