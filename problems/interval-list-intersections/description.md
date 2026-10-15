You are given two lists of closed intervals, `firstList` and `secondList`. Within each list the intervals are pairwise disjoint and sorted by start. Return the intersection of the two lists as a list of closed intervals, sorted by start.

The intersection of two closed intervals is either empty or a closed interval, which may be a single point when they only touch at an endpoint. Either input list may be empty.

Constraints:
- `0 <= len(firstList), len(secondList) <= 1000`
- Endpoints are in `[0, 10^9]` with `start <= end`
- Both lists are already sorted and each list's intervals do not overlap
