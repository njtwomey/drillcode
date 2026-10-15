## The idea

If the numbers split into `k` groups of equal sum, each group sums to `target = total / k`. We could try to pour numbers into `k` buckets with backtracking, but that repeats a lot of work. The bitmask view removes the repeats: the only thing that matters about the numbers used so far is *which* ones they are (a subset), not the order they were placed in.

The trick is to fill buckets one at a time. If we know the total of a subset, then `total % target` tells us how full the bucket currently being filled is, so the "current bucket" needs no extra state.

## Set-up

- Quick rejects: `total % k` non-zero (can't split evenly), or `max(nums) > target` (that number fits in no bucket).
- `fill[mask]`: for the subset of numbers whose bits are set in `mask`, the sum modulo `target`, or `-1` if that subset cannot be laid out as some completely full buckets plus one partly filled bucket.
- `fill[0] = 0`: the empty subset is valid.
- Adding `nums[i]` to a valid subset is allowed only if `fill[mask] + nums[i] <= target`, so the current bucket never overflows. Landing exactly on `target` wraps to 0 and starts a fresh bucket.

```text
nums = [1, 2, 2, 3]    k = 2     total = 8     target = 4
index:  0  1  2  3

fill[{}] = 0     every other entry starts at -1
```

## Step by step

Masks are visited in increasing order. A subset is written by the indices it holds. Only some of the reachable states are shown (the table skips `{2}`, `{0,2}`, `{0,1,3}` and others).

```text
subset      numbers    sum  fill  note
{}          -           0    0    start
{0}         1           1    1
{1}         2           2    2
{3}         3           3    3
{0,1}       1,2         3    3
{1,2}       2,2         4    0    bucket full, wraps to 0
{0,3}       1,3         4    0    bucket full, wraps to 0
{1,3}       2,3         5   -1    2+3 > 4, rejected
{0,1,2}     1,2,2       5    1    {1,2} full, then 1 in the next bucket
{0,1,2,3}   1,2,2,3     8    0    everything placed, no partial bucket
```

From `{0,3}` (fill 0), adding index 1 gives fill 2, then adding index 2 gives `2 + 2 = 4`, which wraps to 0. The full mask ends with `fill == 0`, so the answer is `True` (buckets `{0,3}` = 1 + 3 and `{1,2}` = 2 + 2).

## Why it works

For a subset, `sum % target` is the same however the numbers are ordered, so one entry per subset is enough. Because we never let a bucket exceed `target`, a valid layout is a sequence of full buckets followed by at most one partial one, and the remainder is exactly the partial one's content. Since the total is `k * target`, the full mask has remainder 0 exactly when all `k` buckets are filled exactly.

## Where it goes wrong

- Skipping the checks for `total % k` and for `max(nums) > target`. Without the second, a big number simply never gets added and the full mask is never valid, but the early exit is cheaper and clearer.
- Using `<` rather than `<=` for the overflow check. A bucket must be allowed to reach exactly `target`.
- Storing the raw sum instead of the remainder, which forces you to track which bucket you are in.

```text
{1,3} = numbers 2 and 3 with target 4
  fill 2 + 3 = 5 > 4   -> not stored (-1)
  the number 3 can't go into a bucket that already holds a 2
```

## Cost

Time O(n * 2^n): each of the `2^n` masks tries up to `n` additions. Space O(2^n) for `fill`.
