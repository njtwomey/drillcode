---
title: "Binary search: the two shapes"
area: Binary search
topics: [Binary search]
problems:
  - binary-search
  - first-bad-version
  - search-a-2d-matrix
  - find-minimum-in-rotated-sorted-array
  - search-in-rotated-sorted-array
related: [binary-search-on-answer, opposite-ends]
---
## Reach for it when

- The input is sorted and you need a position, a value or a yes/no in better than O(n).
- The statement says "rotated sorted array".
- A 2D matrix has sorted rows and each row starts above the previous row's last value.
- Some predicate is false for every index up to a point and true from there on ("first bad version").

## Setup

- `lo, hi`: the ends of the range that can still hold the answer. Exact match uses `lo, hi = 0, len(nums) - 1`. First-true uses the same bounds, or `1, n` when the indices are 1-based.
- Loop condition: `while lo <= hi` for exact match (an empty range means not found). `while lo < hi` for first-true (one candidate left means done).
- `mid = (lo + hi) // 2`: the probe. The solutions also write `lo + (hi - lo) // 2`; both give the same result in Python.
- Invariant, exact match: if the target is present it lies in `nums[lo..hi]`, and `mid` is ruled out after it is checked, so the moves are `mid + 1` and `mid - 1`.
- Invariant, first-true: the first true index lies in `[lo, hi]`. When `mid` is true it may be the answer, so `hi = mid`. When it is false, `lo = mid + 1`.

## Template

```python
def first_true(n, predicate):
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo if predicate(lo) else n
```

Exact match is the other shape: `while lo <= hi`, return on equality, otherwise `lo = mid + 1` or `hi = mid - 1`, and `return -1` after the loop. `binary-search` shows it.

## What it removes

It removes the linear scan. Each probe throws away half the range, so n elements take about log2(n) probes. Comparing with `nums[hi]` in the rotated minimum removes the special case for an array that was not rotated at all.

## Pitfalls

- `lo = mid` with `mid = (lo + hi) // 2` never moves when `hi = lo + 1`: infinite loop. For a "last true" search use `mid = (lo + hi + 1) // 2` with `lo = mid` and `hi = mid - 1`.
- Mixing bounds: `hi = n` goes with `while lo < hi` and `hi = mid`; `hi = n - 1` goes with `while lo <= hi` and `hi = mid - 1`. Mixed, the search skips the last element or loops forever.
- Using `hi = mid - 1` in a first-true search discards a `mid` that may be the answer.
- In the rotated minimum, comparing `nums[mid]` with `nums[lo]` fails on an unrotated array. Compare with `nums[hi]`.
- In rotated search, `nums[lo] <= nums[mid]` needs `<=`, not `<`, or a one-element left half is treated as unsorted and the search fails on two-element input.
- `lo + (hi - lo) // 2` only matters in languages with fixed-width integers. Python integers do not overflow.
- First-true when the whole range may be false: `lo` ends at the last index even though it is false, so test the predicate there.

## Variants

- `binary-search`: exact match with inclusive bounds.
- `first-bad-version`: first-true over `[1, n]` with `isBadVersion` as the predicate. This is the template with `lo, hi = 1, n`.
- `find-minimum-in-rotated-sorted-array`: first-true where the predicate is `nums[mid] <= nums[hi]`. If `nums[mid] > nums[hi]` the minimum is to the right, so `lo = mid + 1`; otherwise `hi = mid`. The answer is `nums[lo]`.
- `search-in-rotated-sorted-array`: exact match, plus a test of which half is sorted (`nums[lo] <= nums[mid]`). If the target lies inside the sorted half's bounds, keep that half. Otherwise keep the other.
- `search-a-2d-matrix`: exact match over `0..rows * cols - 1`, with the flat index mapped back by `mid // cols` for the row and `mid % cols` for the column (`divmod(mid, cols)` gives both at once).

## Worked example

Problem: `first-bad-version`

The predicate is the LeetCode-provided `isBadVersion`, and the range is versions 1 to n.

```python
class Solution:
    def firstBadVersion(self, n: int) -> int:
        # Invariant: the first bad version is always within [lo, hi].
        lo, hi = 1, n
        while lo < hi:  # Stop when one candidate is left; it must be the answer.
            mid = lo + (hi - lo) // 2
            if isBadVersion(mid):
                # mid might itself be the first bad one, so keep it in range.
                hi = mid
            else:
                # mid is good, so everything up to and including it is good too.
                lo = mid + 1
        return lo
```

`lo, hi = 1, n` are the template's bounds, shifted to 1-based. `while lo < hi` is the first-true loop. `isBadVersion(mid)` is the predicate, and `hi = mid` keeps a bad `mid` in range. The solution returns `lo` without a final predicate check because the problem guarantees a bad version exists.
