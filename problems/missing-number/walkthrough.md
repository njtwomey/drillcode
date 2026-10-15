## The idea

The array holds `n` distinct numbers taken from `0..n`, so exactly one number in that range is absent. Sorting or a hash set would find it, but there is a neater way: pair up everything that should be there with everything that is, and let the pairs cancel.

XOR does the cancelling. `x ^ x` is 0, `x ^ 0` is `x`, and the order of the operands does not matter. If you XOR all of `0..n` together with all the array's values, every present number appears twice and vanishes. The missing number appears once and is what is left.

## Set-up

- `result` starts at `len(nums)`, which is `n`. The indices only run `0..n-1`, so `n` has no index to pair with; seeding with it covers the range `0..n`.
- Each round folds in the index `i` and the value `num` together.

Invariant: `result` is `n` XOR (indices seen so far) XOR (values seen so far).

## Step by step

Take `nums = [3, 0, 1]`, so `n = 3` and the answer should be 2.

```text
result starts at n = 3

            result   i   num   result ^ i ^ num
Round 1      11      0    3    11 ^ 00 ^ 11  =  00   (0)
Round 2      00      1    0    00 ^ 01 ^ 00  =  01   (1)
Round 3      01      2    1    01 ^ 10 ^ 01  =  10   (2)
```

Written out, the whole computation is `3 ^ (0^3) ^ (1^0) ^ (2^1)`. Regroup it:

```text
numbers 0..3 : 0  1  2  3
array values : 3  0  1
               ──────────
3 cancels 3, 0 cancels 0, 1 cancels 1.   Left over: 2
```

## Why it works

Each number in `0..n` is XORed in once as an index (or as the seed `n`) and once as a value, unless it is the missing one, which has no matching value. Pairs cancel to 0, and XOR with 0 changes nothing, so only the missing number survives.

## Where it goes wrong

Starting `result` at 0 instead of `len(nums)` fails when the missing number is `n`:

```text
nums = [0]      n = 1, answer 1
start 0:   0 ^ 0 ^ 0 = 0       wrong
start 1:   1 ^ 0 ^ 0 = 1       right
```

## Other approaches

`missingNumberSum` uses the fact that `0..n` adds up to `n * (n + 1) // 2`. Subtract the actual `sum(nums)` and the shortfall is the missing number. For `[3, 0, 1]`: 6 minus 4 is 2. It is easier to read; the XOR version just avoids big sums in languages with fixed-width integers.

## Cost

Time O(n), one pass. Space O(1), a single integer.
