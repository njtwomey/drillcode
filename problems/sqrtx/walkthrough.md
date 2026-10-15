## The idea

We want the integer square root of `x`, rounded down: the largest whole number `r` with `r * r <= x`. Trying each `r` from 0 is too slow for big `x`. But the test `r * r <= x` is true for all small `r` and false for all large `r`, with a single switch point in between. A switch point in sorted order is exactly what binary search finds.

## Set-up

- `lo = 0` and `hi = x` bound the answer. For `x >= 1` the root is never larger than `x`, and for `x = 0` the range is just 0.
- `mid` is the guess each round.

Invariant: the answer is always inside `[lo, hi]`. `lo` is always a value whose square is at most `x` (or the starting 0), and everything above `hi` is known to be too big.

## Step by step

Take `x = 10`. The true answer is 3, since 9 <= 10 < 16.

```text
Round 1  lo=0 hi=10  mid=(0+10+1)//2 = 5   25 > 10   too big: hi = 4
Round 2  lo=0 hi=4   mid=(0+4+1)//2  = 2    4 <= 10  ok:      lo = 2
Round 3  lo=2 hi=4   mid=(2+4+1)//2  = 3    9 <= 10  ok:      lo = 3
Round 4  lo=3 hi=4   mid=(3+4+1)//2  = 4   16 > 10   too big: hi = 3
         lo == hi == 3: stop, return 3
```

On the number line:

```text
value   0   1   2   3   4   5 ...
r*r<=10 T   T   T   T   F   F
                    ^ last True: the answer
```

## Why it works

If `mid * mid <= x`, then `mid` is a valid answer and a larger one might exist, so we keep `mid` by setting `lo = mid`. If it is too big, `mid` and everything above it can be thrown away, so `hi = mid - 1`. The range shrinks each round until `lo == hi`, and by the invariant that is the largest valid value.

## Where it goes wrong

The midpoint must round up. Since the success branch sets `lo = mid`, a rounded-down midpoint stalls when `hi = lo + 1`:

```text
x = 1: lo=0 hi=1
  mid = (0+1)//2 = 0   0*0 <= 1   lo = 0   nothing changed: infinite loop
  mid = (0+1+1)//2 = 1 1*1 <= 1   lo = 1   done
```

Also remember the answer rounds down for non-perfect squares: `x = 8` returns 2, not 3. In languages with fixed-width integers, `mid * mid` can overflow for `x` near 2^31; Python's integers do not.

## Cost

Time O(log x): the range halves each round. Space O(1).
