## The idea

For sums, the best subarray ending at each position only needs the best one ending at the previous position. For products it is not enough, because a negative number flips everything. The most negative product so far becomes the largest once multiplied by another negative.

So track two values for subarrays ending at the current index: the largest product and the smallest product.

## Set-up

- `cur_max` and `cur_min` are the largest and smallest product of a subarray ending at the current element. Both start as `nums[0]`.
- `best` is the largest `cur_max` seen. It starts as `nums[0]` too.
- For each next `num` the candidates are: `num` alone (a fresh start), `cur_max * num`, and `cur_min * num`.

## Step by step

`nums = [-2, 3, -4]`.

```text
start      cur_max -2   cur_min -2   best -2

num = 3    candidates: 3, (-2)*3 = -6, (-2)*3 = -6
           cur_max = 3     cur_min = -6     best 3

num = -4   candidates: -4, 3*(-4) = -12, (-6)*(-4) = 24
           cur_max = 24    cur_min = -12    best 24
```

The answer is 24, the whole array. The minimum of `-6` kept from the previous round is what produced it. Without tracking `cur_min` the best seen would be 3.

Zeros restart for free. For `[2, 0, -1]`: at `0`, the candidates are `0, 0, 0`, so both values become 0. At `-1`, the candidates are `-1, 0, 0`, giving `cur_max = 0`, `cur_min = -1`. A zero cannot poison later products because `num` itself is always a candidate.

## Why it works

Any subarray ending here is either just `num`, or an earlier subarray ending at the previous index times `num`. The product with `num` is largest for the earlier max (if `num` is positive) or the earlier min (if `num` is negative), so checking both extremes always finds the best.

## Where it goes wrong

- Updating `cur_max` first and then using the new value to compute `cur_min` is a classic bug. The solution builds the tuple `candidates` once so both updates use the old values.
- Starting `best` at 0 would give the wrong answer for an input like `[-3]`.

## Cost

Time O(n), one pass. Space O(1): a few numbers.
