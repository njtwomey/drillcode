---
title: Math tricks
area: Math
topics: [Array]
problems:
  - powx-n
  - sqrtx
  - happy-number
related: [binary-search-shapes, fast-slow-pointers, bit-tricks]
---
## Reach for it when
- The statement asks for `x ** n` with a large `n`, possibly negative.
- You need an integer square root or other integer root without floating point.
- A number is repeatedly transformed (digit squares, for example) and the question is whether it reaches a fixed point or loops forever.
- A direct loop would take O(n) steps and the structure of the problem (bits of `n`, monotone `r * r`, a bounded sequence) allows fewer.

## Setup
- Exponentiation by squaring: `result = 1.0` and `base = x`. Invariant: `result * base ** n` equals the original `x ** n` for the remaining `n`.
- Make `n` non-negative first: if `n < 0`, set `x = 1 / x` and `n = -n`.
- Each iteration reads the lowest bit with `n & 1`, squares `base`, and shifts `n >>= 1`.
- Integer root: `lo, hi = 0, x`, with the predicate `mid * mid <= x` true for small `mid`. Search for the last true.
- Cycle detection on a sequence: `slow = n`, `fast = next_value(n)`, stepping one and two applications per round.

## Template
```python
def power(x, n):
    if n < 0:
        x = 1 / x
        n = -n
    result = 1.0
    base = x
    while n:
        if n & 1:
            result *= base
        base *= base
        n >>= 1
    return result
```

## What it removes
It removes the O(n) multiplication loop: `x ** n` takes about log2(n) squarings, one per bit. The integer square root removes floating point and its rounding errors, and needs only O(log x) multiplications. Cycle detection removes the set of seen values.

## Pitfalls
- Forgetting the negative exponent: `power(2, -2)` loops forever or returns 1 if the sign is never handled.
- Negating `n = -2**31` overflows in fixed-width languages. Python integers do not, so `powx-n` can negate directly.
- Integer root with `mid = (lo + hi) // 2` and `lo = mid`: it never moves at `hi == lo + 1`. Use the upper midpoint, `(lo + hi + 1) // 2`.
- Setting `hi = mid` in that last-true search drops the `- 1` and loops, or keeps a `mid` that is too large.
- `math.sqrt` on large inputs rounds. Compare `r * r <= x` with integers instead.
- Happy number loop that tests `slow != fast` before the first step: both start apart here (`slow = n`, `fast = next_value(n)`), so the first check is meaningful. If both start at `n`, the loop never runs.
- Stopping only on `fast == 1`: a cycle that excludes 1 then loops forever. The condition needs `slow != fast` as well.

## Variants
- Fast power (`powx-n`): the template. Negative `n` becomes `1 / x` with positive `n`. Bit `k` of `n` folds `x ** (2 ** k)` into `result`.
- Integer square root (`sqrtx`): binary search for the largest `r` with `r * r <= x` over `[0, x]`. This is the last-true shape from `binary-search-shapes`, with `lo = mid` and `hi = mid - 1`. Newton's method (`r = (r + x // r) // 2`) is the other standard route and converges in fewer steps, but the solution uses binary search.
- Digit-square cycle (`happy-number`): `next_value` sums the squares of the digits using `divmod(x, 10)`. The sequence reaches 1 or enters a cycle, because the values stay small. The solution runs Floyd's `slow` and `fast` (as in `fast-slow-pointers`) with no stored values. The file `solution_set.py` stores visited values in `seen` and stops when `n in seen`. Both are correct; the set version uses extra memory.

## Worked example
Problem: `powx-n`

Each bit of the exponent decides whether the current power of `x` joins the answer.

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x = 1 / x
            n = -n
        result = 1.0
        base = x
        while n:
            if n & 1:
                result *= base
            base *= base
            n >>= 1
        return result
```

This is the template inside a class. `result` collects the powers for the set bits, `base` is squared every round, and `n >>= 1` moves to the next bit. For `x = 2`, `n = 10` (binary 1010) the loop multiplies `result` by `base = 4` and then `base = 256`, giving 1024.
