## The idea

A peak is an element larger than both neighbours, and the problem lets us treat whatever lies off either end of the array as negative infinity. The array is not sorted, so ordinary binary search does not apply. But it does not need to be: we only need some peak, and a slope tells us which way to look.

If `nums[mid] < nums[mid + 1]`, the ground rises to the right. Keep walking right while it keeps rising. It must stop rising somewhere, either at a true peak or at the end of the array, which counts as a peak because the outside is negative infinity. So a peak exists to the right.

If it falls to the right, then `mid` is either a peak itself or the ground rose to it from the left, so a peak exists at `mid` or earlier.

## Set-up

- `lo` and `hi` bound a window that is guaranteed to contain a peak. They start as the full array.

Invariant: `[lo, hi]` always contains a peak. The outer neighbours are `-infinity`, so the window edges can never rule a peak out.

```text
nums = [1, 2, 1, 3, 5, 6, 4]
index    0  1  2  3  4  5  6
         ▲              ▲  
         lo             hi    (the cells beyond both ends are -inf)
```

## Step by step

```text
Round 1  lo=0 hi=6  mid=3   nums[3]=3 < nums[4]=5   rising
         peak is right of mid.  lo = 4

                        lo    hi
         [1  2  1  3 |  5  6  4]

Round 2  lo=4 hi=6  mid=5   nums[5]=6 < nums[6]=4 ?  no, falling
         peak is at mid or left.  hi = 5

Round 3  lo=4 hi=5  mid=4   nums[4]=5 < nums[5]=6   rising
         lo = 5

lo == hi == 5, return 5.   nums[5] = 6, bigger than 5 and 4.
```

The array also has a peak at index 1 (value 2). Any peak is accepted, and this search happened to find the other one.

## Why it works

The window always holds a peak. When the slope at `mid` rises, climbing right from `mid + 1` ends at a peak inside the window. When it falls, climbing left from `mid` (or stopping at `mid`) ends at one. Both moves keep a peak inside, and the window shrinks every round, so it collapses onto a single cell that must be a peak.

## Where it goes wrong

Comparing with the left neighbour `nums[mid - 1]` risks an index of `-1`, which silently wraps in Python. Comparing `mid` with `mid + 1` is safe because `mid < hi <= len(nums) - 1`.

Setting `hi = mid - 1` in the falling case loses `mid`, which may be the only peak.

```text
[1, 3, 2]   lo=0 hi=2 mid=1: 3 < 2? no, falling.
            hi = mid - 1 = 0 would discard index 1, the only peak.
            hi = mid = 1 keeps it.
```

Equal neighbours cannot happen because the problem guarantees adjacent values differ.

## Cost

Time O(log n): the window halves each round. Space O(1).
