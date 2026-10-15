You are given `prices`, where `prices[i]` is a stock's price on day `i`. You may complete as many buy-then-sell transactions as you like, holding at most one share at a time. After selling, you cannot buy on the very next day; one cooldown day is required. Return the maximum total profit, which is 0 if no profitable trade exists.

Constraints:
- `1 <= len(prices) <= 5000`
- `0 <= prices[i] <= 1000`
- Linear time is possible; exhaustive search over trade sequences is not
