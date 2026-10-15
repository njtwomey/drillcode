There are `n` cities labelled `0..n - 1` and directed flights `flights[i] = [from, to, price]`. Given `src`, `dst` and an integer `k`, return the cheapest total price of a trip from `src` to `dst` that makes at most `k` stops, meaning at most `k + 1` flights. Return `-1` if there is no such trip.

Constraints:
- `1 <= n <= 100`
- `0 <= len(flights) <= n * (n - 1) / 2`
- `1 <= price <= 10^4`
- `0 <= k < n`, `src != dst`
- No two flights share the same `from` and `to`.
