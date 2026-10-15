---
title: Binary search on the answer
area: Binary search
topics: [Binary search]
problems:
  - koko-eating-bananas
  - longest-increasing-subsequence
related: [binary-search-shapes, dp-space-and-loop-order]
---
## Reach for it when

- The statement asks for "the minimum speed / capacity / size such that ..." or "the maximum ... such that ...".
- The answer is a number, and you can check whether a given number works in one pass over the input.
- A bigger number never makes a feasible answer infeasible (or the reverse). The check flips once from false to true.

## Setup

- `lo, hi`: the smallest and largest answers that could possibly work. Koko uses `1` and `max(piles)`.
- A `feasible(x)` check that returns whether answer `x` works. It costs O(n).
- The first-true loop from `binary-search-shapes` over `[lo, hi]`: `while lo < hi`, `mid = (lo + hi) // 2`, `hi = mid` if `feasible(mid)`, else `lo = mid + 1`.
- Invariant: the smallest feasible answer is always in `[lo, hi]`.

## Template

```python
def min_feasible(lo, hi, feasible):
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

## What it removes

It removes searching the input or trying every candidate answer. The check costs O(n) and the search needs O(log range) checks, so Koko is O(n log max(piles)) instead of O(n * max(piles)).

## Pitfalls

- `hi` too small. For Koko the speed `max(piles)` always works, so it is a safe upper bound; anything smaller can miss the answer.
- `lo` too small is harmless but wasteful; `lo = 0` can divide by zero inside the check.
- A predicate that is not monotone. If feasibility flips back and forth, this is the wrong tool and the search returns a wrong answer on some inputs.
- Integer ceiling: `(pile + mid - 1) // mid` is `ceil(pile / mid)`. Using `pile // mid` undercounts the hours for a partial pile.
- LIS: the `tails` list is not the subsequence. Only its length is meaningful.
- LIS: `bisect_right` instead of `bisect_left` lets equal values extend the run, which is wrong for a strictly increasing subsequence (`[2, 2]` would give 2).

## Variants

- `koko-eating-bananas`: search the speed. The check sums `ceil(pile / speed)` over the piles and compares it with `h`.
- `longest-increasing-subsequence`: a different use of binary search, on a list the algorithm builds. `tails[i]` is the smallest possible last value of an increasing subsequence of length `i + 1`. For each `num`, `bisect_left(tails, num)` finds the first tail `>= num`. Replace it, or append when none is found. `tails` stays sorted, which is why it can be searched. The length of `tails` is the answer. The solution also keeps an O(n^2) DP version as `lengthOfLISQuadratic`.

## Worked example

Problem: `koko-eating-bananas`

The search runs over speeds, not over `piles`.

```python
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # Answer lies in [1, max(piles)]: max(piles) always works (one pile per hour,
        # given h >= len(piles)), and speed 0 is meaningless.
        lo, hi = 1, max(piles)
        while lo < hi:
            # Invariant: the answer is in [lo, hi]. Faster speed never hurts, so
            # "feasible" flips from False to True exactly once as speed grows.
            mid = (lo + hi) // 2
            # (pile + mid - 1) // mid is integer ceil(pile / mid): a partial pile
            # still costs a whole hour.
            hours = sum((pile + mid - 1) // mid for pile in piles)
            if hours <= h:
                hi = mid  # mid works, but a slower speed might too; keep it
            else:
                lo = mid + 1  # mid is too slow, so everything <= mid is too
        return lo  # lo == hi: the smallest feasible speed
```

`lo, hi = 1, max(piles)` are the bounds. The `hours` sum is `feasible(mid)`, written inline as `hours <= h`. The branch `hi = mid` / `lo = mid + 1` is the template's first-true step. The solution returns `lo` when `lo == hi`.
