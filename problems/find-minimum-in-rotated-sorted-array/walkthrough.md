## The idea

A sorted array that has been rotated is two sorted runs glued together, with one drop in the middle. The smallest value is right after that drop. Scanning for it is O(n); we can do better because half of any window is always still sorted.

The question to ask each step is: is the drop to the right of `mid`, or at or to the left of it? One comparison answers it, and either answer lets us throw away half of the window.

## Set-up

- `lo` and `hi` bound the window that must contain the minimum. They start as the whole array.

Invariant: the minimum is always inside `[lo, hi]`. The loop runs while `lo < hi` and stops when the window is a single cell, which is the minimum.

```text
nums = [4, 5, 6, 7, 0, 1, 2]
index    0  1  2  3  4  5  6
         ▲              ▲
         lo             hi
```

## Step by step

Compare `nums[mid]` with `nums[hi]`, not with `nums[lo]`.

```text
Round 1  lo=0 hi=6  mid=3   nums[mid]=7 > nums[hi]=2
         7 is larger than the right end, so the drop is right of mid.
         lo = mid + 1 = 4

                      lo       hi
         [4  5  6  7 | 0  1  2]

Round 2  lo=4 hi=6  mid=5   nums[mid]=1 <= nums[hi]=2
         This part is sorted, so the minimum is at mid or left of it.
         hi = mid = 5

Round 3  lo=4 hi=5  mid=4   nums[mid]=0 <= nums[hi]=1
         hi = mid = 4

lo == hi == 4, return nums[4] = 0.
```

## Why it works

If `nums[mid] > nums[hi]`, then reading from `mid` to `hi` goes down somewhere, so the drop (and the minimum) lies strictly right of `mid`. We can discard `mid` too and set `lo = mid + 1`.

If `nums[mid] <= nums[hi]`, the stretch from `mid` to `hi` has no drop in it, so it is sorted, and nothing right of `mid` can be smaller than `nums[mid]`. The minimum is `mid` or to its left, so `hi = mid`.

Using `hi` as the reference also covers an array that was never rotated: then `nums[mid] <= nums[hi]` every time, `hi` keeps shrinking, and `lo` ends at index 0.

## Where it goes wrong

Writing `hi = mid - 1` in the second branch. `mid` might itself be the minimum (as at round 3), and this throws it away.

Comparing with `nums[lo]` instead needs an extra case for the unrotated array, because `nums[mid] >= nums[lo]` holds there but says nothing useful about where the minimum is.

```text
[1, 2, 3, 4, 5]   mid=2: nums[mid]=3 >= nums[lo]=1
                  "go right" would walk away from the minimum at index 0
```

## Cost

Time O(log n): the window halves each round. Space O(1): two indices. This relies on distinct values; with duplicates `nums[mid] == nums[hi]` becomes ambiguous.
