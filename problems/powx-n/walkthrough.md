## The idea

Multiplying `x` by itself `n` times takes `n` steps, hopeless when `n` is around two billion. But squaring gets you far, fast: x, x^2, x^4, x^8, and so on, each from the previous with one multiplication.

Any exponent is a sum of powers of two, which is just its binary form. For example 10 = 8 + 2, so x^10 = x^8 * x^2. Walk through the bits of `n`, keep squaring, and multiply the current square into the answer when the bit is set. That is about 31 steps at most.

## Set-up

- If `n` is negative, flip it: `x = 1 / x` and `n = -n`. Since x^-n is the same as (1/x)^n, the loop only handles non-negative exponents. Python ints do not overflow, so negating the most negative value is safe.
- `result` is the answer so far, starting at 1.0 (the empty product).
- `base` holds x^(2^k) for the bit k we are looking at. It starts as `x`.

```text
x = 2, n = 10       n in binary: 1010

result = 1.0
base   = 2.0        (2^1)
```

## Step by step

Each round looks at the lowest bit with `n & 1`, squares `base`, and shifts `n` right.

```text
n (bin)  low bit  action              result   base
1010       0      skip                  1       4      (2^2)
 101       1      result *= 2^2         4       16     (2^4)
  10       0      skip                  4       256    (2^8)
   1       1      result *= 2^8       1024      65536
   0     loop ends
```

The answer is `1024.0`, which is 2^10. The set bits were worth 2^2 and 2^8, and 4 * 256 = 1024.

For a negative power, say `x = 2`, `n = -2`: `x` becomes 0.5, `n` becomes 2, and the loop gives 0.25.

## Why it works

Writing n in binary as the sum of its set bits, x^n is the product of x^(2^k) over the set bits k. `base` is exactly x^(2^k) at step k, since each squaring doubles the exponent. The shift moves to the next bit, so every bit is looked at once.

## Where it goes wrong

- Forgetting to square `base` on rounds where the bit is 0. Then `base` falls behind and the next set bit multiplies by the wrong power.
- Handling negatives by computing the power first and inverting at the end can overflow the intermediate value to infinity for a large exponent. Inverting `x` first avoids that.
- `n = 0` should give 1.0: the loop never runs, and `result` is still 1.0.

## Cost

Time O(log n), one loop round per bit of the exponent. Space O(1): three variables.
