---
title: Math tricks
area: Maths
topics: [Array, String, Maths]
problems:
  - powx-n
  - sqrtx
  - happy-number
  - plus-one
  - add-binary
  - multiply-strings
  - reverse-integer
  - string-to-integer-atoi
related: [binary-search-shapes, fast-slow-pointers, bit-tricks, dp-state-machines]
---
## Reach for it when
- The statement asks for `x ** n` with a large `n`, possibly negative.
- You need an integer square root or other integer root without floating point.
- A number is repeatedly transformed (digit squares, for example) and the question is whether it reaches a fixed point or loops forever.
- Numbers arrive as digit arrays or digit strings, and the sum or product must be built digit by digit with a carry (`plus-one`, `add-binary`, `multiply-strings`).
- The result must stay inside a 32-bit range although the language has unbounded integers (`reverse-integer`, `string-to-integer-atoi`).
- A direct loop would take O(n) steps and the structure of the problem (bits of `n`, monotone `r * r`, a bounded sequence) allows fewer.

## Setup
- Exponentiation by squaring: `result = 1.0` and `base = x`. Invariant: `result * base ** n` equals the original `x ** n` for the remaining `n`.
- Make `n` non-negative first: if `n < 0`, set `x = 1 / x` and `n = -n`.
- Each iteration reads the lowest bit with `n & 1`, squares `base`, and shifts `n >>= 1`.
- Integer root: `lo, hi = 0, x`, with the predicate `mid * mid <= x` true for small `mid`. Search for the last true.
- Cycle detection on a sequence: `slow = n`, `fast = next_value(n)`, stepping one and two applications per round.
- Digit arithmetic: walk from the least significant digit, keep a `carry` that is 0 or 1 (for products, a value below 10 carried into the next column), and write `total % base` and carry `total // base`.
- 32-bit bound: a `limit` that is `2**31 - 1` or, for negatives, `2**31`. Decide the sign first, work on the absolute value, and test before each append.

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
- Forgetting the final carry in digit addition. `add-binary` on `"1"` and `"1"` must give `"10"`; the loop condition `i >= 0 or j >= 0 or carry` is what keeps it running one more round. `plus-one` on `[9, 9, 9]` needs the new leading 1.
- Peeling digits of a negative number with `//` and `%`. Python floors, so `-123 // 10` is `-13`. `reverse-integer` takes `abs(x)` and reapplies `sign` at the end.
- Checking the 32-bit bound after the append. Python never overflows, so a late check works, but the check-before form is `result > (limit - digit) // 10`; the limit differs by sign (`2**31` for negatives).
- Product columns that overflow a digit. In `multiply-strings` add the partial product into the existing column value before splitting with `% 10` and `// 10`, otherwise carries are lost; also return `"0"` early, or the result keeps leading zeros.
- Stopping only on `fast == 1`: a cycle that excludes 1 then loops forever. The condition needs `slow != fast` as well.

## Variants
- Fast power (`powx-n`): the template. Negative `n` becomes `1 / x` with positive `n`. Bit `k` of `n` folds `x ** (2 ** k)` into `result`.
- Integer square root (`sqrtx`): binary search for the largest `r` with `r * r <= x` over `[0, x]`. This is the last-true shape from `binary-search-shapes`, with `lo = mid` and `hi = mid - 1`. Newton's method (`r = (r + x // r) // 2`) is the other standard route and converges in fewer steps, but the solution uses binary search.
- Carry stops early (`plus-one`): scan from the right; a digit below 9 is incremented and the function returns at once. Each 9 becomes 0. If the loop finishes, every digit was 9 and the answer is `[1] + digits`.
- Carry through two strings (`add-binary`): indices `i` and `j` start at the last characters, `total` is `carry` plus the bits that exist, `digits.append(str(total % 2))`, `carry = total // 2`. The result is reversed at the end, with `or "0"` for the empty case.
- Schoolbook product (`multiply-strings`): `result = [0] * (m + n)`; digit `i` of `num1` times digit `j` of `num2` goes into column `i + j + 1`, with the carry added to column `i + j`. At most one leading zero is dropped.
- Digit peeling with a bound (`reverse-integer`): `x, digit = divmod(x, 10)`, then `result = result * 10 + digit` unless `result > (limit - digit) // 10`, which returns 0.
- Parse then clamp (`string-to-integer-atoi`): digits accumulate into `result`, growth stops once it passes `2**31`, and the end is `max(INT_MIN, min(INT_MAX, sign * result))`. The phases are described in `dp-state-machines`.
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
