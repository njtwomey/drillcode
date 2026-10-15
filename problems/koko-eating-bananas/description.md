Given pile sizes `piles` and an hour budget `h` (with `h >= len(piles)`), choose an integer eating speed `k` bananas per hour. Each hour you pick one pile and eat up to `k` bananas from it; if the pile has fewer than `k`, you finish it and the rest of that hour is wasted. Return the minimum `k` that finishes every pile within `h` hours.

Constraints:
- `1 <= len(piles) <= 10^4`
- `1 <= piles[i] <= 10^9`
- `len(piles) <= h <= 10^9`
