"""Pow(x, n) (#50, medium)

Approach: Binary exponentiation; square the base each step and multiply it in for every
    set bit of the exponent.
Tricks: Invert x and negate n for a negative exponent; Python ints make negating -2^31
    safe.
Edge cases:
  - n = 0 gives 1
  - Negative exponent
  - Negative base with odd exponent
  - n = -2^31

Time O(log n), space O(1).
"""

class Solution:
    def myPow(self, x: float, n: int) -> float:
        # A negative exponent means the reciprocal of the positive power. Python ints
        # do not overflow, so negating n = -2^31 is safe here.
        if n < 0:
            x = 1 / x
            n = -n
        # Binary exponentiation: write n in binary. Each set bit k contributes x^(2^k),
        # and base squares once per bit, so only about log2(n) multiplications.
        result = 1.0
        base = x
        while n:
            if n & 1:  # this bit of the exponent is set: fold the current power in
                result *= base
            base *= base
            n >>= 1
        return result
