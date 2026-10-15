Given a positive integer `n`, return the smallest number of perfect squares (1, 4, 9, 16, ...) whose sum is exactly `n`. The same square may be used repeatedly. Since 1 is a perfect square, an answer always exists.

Constraints:
- `1 <= n <= 10^4`
- Trying all combinations of squares is exponential; roughly O(n * sqrt(n)) time is expected
- Taking the largest square that fits at every step is not always optimal
