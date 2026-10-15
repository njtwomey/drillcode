## The idea

Summing `nums[left..right]` directly is O(n) per query, which hurts when there are many queries on the same array. Because the array never changes, we can pay once up front. Precompute running totals; then any range sum is the difference of two totals.

Picture a running tally: if you know the total up to `right` and the total up to just before `left`, the part in between is the gap between them.

## Set-up

- `self.prefix` is built in the constructor. `prefix[i]` is the sum of the first `i` numbers, `nums[:i]`.
- It starts as `[0]`. That leading 0 is the sum of zero numbers, and it means a range beginning at index 0 needs no special handling. It also makes `prefix` one element longer than `nums`.

Invariant: `prefix[-1]` is always the sum of all numbers processed so far, so the next entry is `prefix[-1] + num`.

## Step by step

Building from `nums = [-2, 0, 3, -5, 2, -1]`:

```text
nums    :     -2    0    3   -5    2   -1
prefix  : 0   -2   -2    1   -4   -2   -3
index   : 0    1    2    3    4    5    6
```

`prefix[3]` is `-2 + 0 + 3 = 1`: the sum of the first three numbers.

Queries use `prefix[right + 1] - prefix[left]`:

```text
sumRange(0, 2)   prefix[3] - prefix[0] =  1 - 0     =  1
sumRange(2, 5)   prefix[6] - prefix[2] = -3 - (-2)  = -1
sumRange(0, 5)   prefix[6] - prefix[0] = -3 - 0     = -3
```

A picture of the second query:

```text
nums       -2   0 |  3   -5    2   -1
prefix  0  -2  -2 |  1   -4   -2   -3
                ^                  ^
            prefix[2]          prefix[6]
the total up to here is subtracted from the total up to there
```

## Why it works

`prefix[right + 1]` adds `nums[0..right]` and `prefix[left]` adds `nums[0..left-1]`. Subtracting cancels the shared part, leaving exactly `nums[left..right]`. Negative numbers are no problem, since the subtraction is exact.

## Where it goes wrong

Off-by-one on the index. The entry for `nums[right]` lives at `prefix[right + 1]` because of the leading 0. Using `prefix[right]` would drop the last element.

```text
sumRange(0, 2) with prefix[right]:  prefix[2] - prefix[0] = -2   wrong (misses 3)
with prefix[right + 1]:             prefix[3] - prefix[0] =  1   right
```

A single-element range works naturally: `sumRange(i, i)` is `prefix[i + 1] - prefix[i]`, which is `nums[i]`.

## Cost

Building is O(n) time. Each query is O(1) time. Space is O(n) for the prefix array.
