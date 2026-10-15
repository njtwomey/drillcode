## The idea

If the array is sorted, one comparison with the middle element lets you throw away half of it. If `nums[mid]` is too small, the target can only be to the right; if too big, only to the left. Halving repeatedly takes about log2(n) steps instead of n.

## Set-up

- `lo` and `hi` are inclusive bounds of the window that might still hold the target. They start at `0` and `len(nums) - 1`.
- `mid` is the probe, `lo + (hi - lo) // 2`.

Invariant: if the target exists, its index is in `lo..hi`. The loop runs while `lo <= hi`, so a window of exactly one element is still examined.

```text
nums:  -1   0   3   5   9  12        target = 9
idx:    0   1   2   3   4   5
        ^                   ^
        lo                  hi
```

## Step by step

```text
Round 1   mid = 0 + (5 - 0) // 2 = 2     nums[2] = 3 < 9, so lo = mid + 1

nums:  -1   0   3   5   9  12
idx:    0   1   2   3   4   5
                    ^       ^
                    lo      hi        (indices 0..2 discarded)

Round 2   mid = 3 + (5 - 3) // 2 = 4     nums[4] = 9 == target
          return 4
```

A miss shows the other exit. Searching for `2` in `[-1, 0, 3, 5, 9, 12]`:

```text
lo=0 hi=5 mid=2  3 > 2   hi = 1
lo=0 hi=1 mid=0  -1 < 2  lo = 1
lo=1 hi=1 mid=1   0 < 2  lo = 2
lo=2 hi=1        lo > hi, window empty, return -1
```

## Why it works

Every comparison either finds the target or proves it is not at `mid` and not on the wrong side, so the window shrinks without ever losing the target. The window gets strictly smaller each round (it loses at least `mid`), so the loop ends. When it is empty, nothing is left to check.

## Where it goes wrong

Mixing bounds styles. This version has `hi` inclusive, so it needs `lo <= hi` and `hi = mid - 1`. Using `hi = mid` here, or `<` in the loop condition, can skip the last element or loop forever:

```text
lo = 2, hi = 3, mid = 2, nums[2] < target
wrong: lo = mid       -> lo stays 2, same window forever
right: lo = mid + 1   -> lo = 3, window shrinks
```

## Cost

Time O(log n): the window halves each round. Space O(1).
