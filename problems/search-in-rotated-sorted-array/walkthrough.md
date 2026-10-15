## The idea

A rotated sorted array looks like two sorted runs glued together, with a drop where the old end meets the old start. Plain binary search breaks because comparing `target` with the middle no longer tells you which side to keep.

The rescue is that at any middle, at least one of the two halves is cleanly sorted. A sorted half has known bounds, so you can say for certain whether `target` lies in it. If yes, go there. If no, it must be in the other half. That keeps the halving, so it stays O(log n), where a scan would be O(n).

## Set-up

- `lo`, `hi` bound the live range. Invariant: if `target` is in the array, its index is in `[lo, hi]`.
- `mid` is the probe. It is checked first, so afterwards it is known not to be the answer.

```text
nums = [4, 5, 6, 7, 0, 1, 2]     target = 0
index:  0  1  2  3  4  5  6
        ^lo          ^mid      ^hi        (lo=0, mid=3, hi=6)
```

## Step by step

How do we know which half is sorted? If `nums[lo] <= nums[mid]`, the left half has no drop in it, so it is sorted. Otherwise the drop is on the left, and the right half is sorted.

```text
Round 1   lo=0 mid=3 hi=6     nums[mid]=7, not the target
          nums[lo]=4 <= 7, so the LEFT half [4,5,6,7] is sorted.
          Is 4 <= 0 < 7?  No.  So target is on the right:  lo = mid + 1 = 4

          [4, 5, 6, 7 | 0, 1, 2]
           x  x  x  x   ^lo   ^hi

Round 2   lo=4 mid=5 hi=6     nums[mid]=1, not the target
          nums[lo]=0 <= 1, so the left half [0,1] is sorted.
          Is 0 <= 0 < 1?  Yes.  So:  hi = mid - 1 = 4

          [4, 5, 6, 7 | 0 | 1, 2]
                       ^lo
                       ^hi

Round 3   lo=4 mid=4 hi=4     nums[mid]=0 == target, return 4
```

## Why it works

The array has at most one drop. The probe at `mid` either sits left of it (then everything from `lo` to `mid` is in order) or right of it (then everything from `mid` to `hi` is in order). Whichever half is sorted, the test `nums[lo] <= target < nums[mid]` (or `nums[mid] < target <= nums[hi]` for the right half) is exact. The bounds are exclusive on the `mid` side because `mid` was already ruled out. If the target fails the sorted half's test, it cannot be there, so the other half is all that remains.

## Where it goes wrong

- Using `<` in `nums[lo] <= nums[mid]`. When the range has two elements, `lo == mid`, and a one-element left half is still sorted. With `<` you would treat it as the right-sorted case and discard the wrong side.

```text
nums = [3, 1], target = 1
lo=0, mid=0, hi=1
nums[lo] <= nums[mid]  (3 <= 3) -> left half [3] is sorted
3 <= 1 < 3?  No  ->  lo = 1.  Next round finds 1 at index 1.
```

- Making the target test inclusive at `mid`. It would keep an index we already rejected. The sorted-half bound on the `mid` side must be strict.
- An array that is not rotated at all still works: the left half is always sorted.

## Cost

Time O(log n): one half is dropped per round. Space O(1).
