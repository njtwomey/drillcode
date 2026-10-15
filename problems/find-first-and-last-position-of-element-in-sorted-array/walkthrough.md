## The idea

In a sorted array every copy of the target sits in one block. We need the block's two ends. A linear scan is O(n), but sorted data means binary search is available.

Plain binary search finds some copy of the target, not the first or the last. Searching for the edges directly leads to two fiddly, slightly different loops. A neater way is to write one search, `lower_bound(x)`, the first index whose value is at least `x`, and use it twice:

- The first copy of `target` is at `lower_bound(target)`.
- The slot just after the last copy is where the first value greater than `target` starts, which for integers is `lower_bound(target + 1)`. Subtract one to land on the last copy.

## Set-up

Inside `lower_bound`, `lo` and `hi` bound a half-open range `[lo, hi)`. They start at `0` and `len(nums)`, so the answer may be `len(nums)` when every value is smaller than `x`.

Invariant: everything left of `lo` is `< x`, and everything from `hi` onward is `>= x`. The answer is always in `[lo, hi]`.

```text
nums = [5, 7, 7, 8, 8, 10]      target = 8
index   0  1  2  3  4  5
```

## Step by step

First `lower_bound(8)`:

```text
lo=0 hi=6  mid=3  nums[3]=8   not < 8   hi = 3
lo=0 hi=3  mid=1  nums[1]=7   < 8       lo = 2
lo=2 hi=3  mid=2  nums[2]=7   < 8       lo = 3
lo=3 hi=3  stop                          first = 3
```

`nums[3] == 8`, so the target exists. Now `lower_bound(9)`:

```text
lo=0 hi=6  mid=3  nums[3]=8   < 9       lo = 4
lo=4 hi=6  mid=5  nums[5]=10  not < 9   hi = 5
lo=4 hi=5  mid=4  nums[4]=8   < 9       lo = 5
lo=5 hi=5  stop                          returns 5
```

So `last = 5 - 1 = 4`, and the answer is `[3, 4]`.

```text
index   0  1  2  3  4  5
nums   [5  7  7  8  8  10]
                 ▲  ▲
               first last
```

## Why it works

`lower_bound(x)` marks the boundary between values below `x` and values at or above it. For `target` that boundary is the start of the block. For `target + 1` it is the end of the block plus one, because integers leave no room between `target` and `target + 1`. Both searches are ordinary O(log n) loops.

## Where it goes wrong

Skipping the existence check. `lower_bound(target)` always returns something, even when the target is absent. So test `first == len(nums) or nums[first] != target` before computing `last`, and return `[-1, -1]` otherwise. Without the first half of that test, `nums[first]` is out of range when the target is bigger than everything.

The other trap is `hi = len(nums) - 1` instead of `len(nums)`, which can never return the end slot.

## Cost

Time O(log n): two binary searches. Space O(1).
