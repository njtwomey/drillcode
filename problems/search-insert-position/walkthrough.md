## The idea

We want the index of `target` in a sorted list, or the index where it would have to be inserted to keep the list sorted. Both are the same thing: the first position whose value is at least `target`. Everything before that position is smaller, everything from it onwards is not. Because the array is sorted, "is this value smaller than the target?" flips from true to false exactly once, so binary search can find the flip in O(log n) instead of scanning.

## Set-up

- `lo = 0` and `hi = len(nums)`. The answer lives in the range `[lo, hi]`, and `hi` is allowed to equal `len(nums)` because a target bigger than everything is inserted at the end.
- `mid` is the middle of the current range.

Invariant: every index below `lo` holds a value smaller than `target`, and every index at or above `hi` holds a value that is at least `target`. The loop ends when `lo == hi`, and that common value is the answer.

```text
nums = [1, 3, 5, 6]    target = 2
index:  0  1  2  3  4
        1  3  5  6  |
        lo          hi
```

## Step by step

```text
Round 1  lo=0 hi=4 mid=2   nums[2]=5 >= 2   so hi = 2
         [1, 3, 5, 6]
          lo    hi
                mid

Round 2  lo=0 hi=2 mid=1   nums[1]=3 >= 2   so hi = 1
         [1, 3, 5, 6]
          lo hi
             mid

Round 3  lo=0 hi=1 mid=0   nums[0]=1 <  2   so lo = 1
         [1, 3, 5, 6]
          lo = 1, hi = 1: the range is empty, stop
```

`lo == hi == 1`, so return 1. Inserting 2 at index 1 gives `[1, 2, 3, 5, 6]`.

With `target = 7`, everything is smaller: `lo` climbs to 3 (since 5 < 7), then to 4 (since 6 < 7), and `hi` was already 4, so the answer is 4, the end of the array.

## Why it works

When `nums[mid] < target`, `mid` and everything left of it are too small, so the answer is at least `mid + 1`. When `nums[mid] >= target`, `mid` could itself be the answer, so `hi = mid` keeps it in range. The range shrinks every round and both rules preserve the invariant.

## Where it goes wrong

Starting `hi` at `len(nums) - 1` makes the end position unreachable:

```text
nums = [1, 3, 5, 6]   target = 7
hi = 3:  lo climbs to 3, loop stops, returns 3
          but 6 < 7, so the true answer is 4
```

Also, `hi = mid` (not `mid - 1`) is required with this `lo < hi` loop; `mid - 1` could skip the answer. A single-element array works: `[5]` with target 5 gives `mid=0`, `5 >= 5`, `hi=0`, return 0.

## Cost

Time O(log n): the range halves each round. Space O(1).
