Implement `myPow(x, n)`, returning `x` raised to the integer power `n` as a float, without using the built-in power operator or `pow`. The exponent may be negative, in which case the result is `1 / x^|n|`.

Answers are compared with a small floating-point tolerance. Exponent magnitudes are large enough that multiplying `x` by itself `n` times is too slow.

Constraints:
- `-100.0 < x < 100.0`
- `-2^31 <= n <= 2^31 - 1`
- Either `x` is nonzero or `n > 0`
- The result fits in `[-10^4, 10^4]`
