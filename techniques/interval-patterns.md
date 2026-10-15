---
title: Interval patterns
area: Intervals
topics: [Intervals]
problems:
  - merge-intervals
  - insert-interval
  - non-overlapping-intervals
  - meeting-rooms
  - meeting-rooms-ii
  - interval-list-intersections
  - minimum-number-of-arrows-to-burst-balloons
  - minimum-interval-to-include-each-query
related: [heap-patterns, greedy-one-pass-invariants, opposite-ends]
---
## Reach for it when

- The input is a list of intervals, meetings, ranges or schedules given as `[start, end]` pairs.
- The question is about overlap: merge, count conflicts, remove the fewest, find a gap, or count how many are active at once.
- Many point queries ask which interval covers them, and the queries can be answered in any order.
- Comparing every pair would be O(n^2) and the data can be sorted first.

## Setup

- Sort first. The real decision is the sort key.
  - By start: merging, overlap detection, inserting, and room counting with a heap.
  - By end: the largest set of non-overlapping intervals, equivalently the fewest removals.
- `result = []`: the merged or kept intervals. Invariant: it is sorted and disjoint, so a new interval can only touch `result[-1]`.
- `last_end`: the end of the last kept interval, for the by-end greedy. Invariant: everything kept so far ends at or before it.
- A heap `ends` of end times, for counting rooms. Invariant: it holds the end times of the meetings currently running; its size is the number in use.
- Two sorted, disjoint lists need no sort: two indexes `i` and `j`, one per list. Invariant: everything before `i` and `j` has been matched against all it can overlap.
- Overlap test for two intervals: `a[0] <= b[1] and b[0] <= a[1]`. After sorting by start, only `next.start <= last.end` is needed.
- Decide the touching rule from the problem, not by habit. `[1, 4]` and `[4, 5]` merge in merge-intervals, but back-to-back meetings do not conflict.

## Template

```python
def merge_overlapping(intervals):
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result
```

`merge_overlapping([[1, 3], [8, 10], [2, 6], [6, 7]])` returns `[[1, 7], [8, 10]]`. Change `<=` to `<` when touching intervals must stay separate.

## What it removes

- All-pairs overlap checks. Once sorted by start, an interval can only overlap the last one in `result`, so one comparison per interval is enough.
- Case analysis over how two intervals overlap (contained, left overlap, right overlap). Taking `max` of the ends covers them all.
- A search for the best interval to keep. Sorting by end makes the earliest-finishing choice the greedy one, so a single pass with `last_end` suffices.

## Pitfalls

- Sorting by start when the greedy needs end. On `[[1, 10], [2, 3], [4, 5]]` start order keeps `[1, 10]` first and removes two intervals instead of one.
- The wrong touching rule. `<` where `<=` is needed leaves `[1, 4]` and `[4, 5]` unmerged; `<=` where `<` is needed reports back-to-back meetings as conflicts.
- Assigning the end instead of taking `max` when merging. `[[1, 10], [2, 3]]` shrinks to `[1, 3]`.
- Empty input. Indexing `intervals[0]` fails; guard it if the constraints allow zero intervals.
- Advancing the wrong pointer when intersecting two lists. Move the interval that ends first; moving the other can skip an overlap with the next interval. Advancing both on every step misses `[[1, 10]]` against `[[2, 3], [4, 5]]`.
- Testing `lo < hi` for an intersection. Intervals that touch at one point, such as `[1, 2]` and `[2, 3]`, then lose the overlap `[2, 2]`.
- Using `>=` where `>` is needed in the arrows count. Balloons `[1, 2]` and `[2, 3]` share an arrow at 2, so a new arrow is needed only when `start > arrow_x`; with `>=` the answer is one too high.
- In `minimum-interval-to-include-each-query`, answering queries in input order, or writing answers by sorted position. Sort `(q, idx)` pairs and store at `result[idx]`; queries may repeat.
- In the same problem, leaving an interval on the heap whose end is before `q`. Pop while `heap[0][1] < q` before reading the root, or the answer can be an interval that ended earlier.
- Using `<` in the sweep with separate sorted starts and ends when the touching rule says an ending meeting frees its room. Use `s >= ends[j]`.

## Variants

- Merge, `merge-intervals`: the template. Sort by start, extend the last interval or append. Touching counts as overlap.
- Insert into a sorted list, `insert-interval`: no sort, because the input is already sorted and disjoint. One pass, three phases. Copy intervals that end before the new start; absorb every interval that starts at or before the new end by taking `min` of starts and `max` of ends; then emit the new interval and the rest.
- Keep the most, `non-overlapping-intervals`: sort by end, keep an interval when `start >= last_end` and update `last_end`, otherwise count a removal. Touching is fine here.
- Detect any conflict, `meeting-rooms`: sort by start and compare each start with the previous end. Strict `<`, since back-to-back is allowed.
- Count the peak, `meeting-rooms-ii`: sort by start and keep a min-heap of end times; reuse the room whose end is at or before the next start. Or sort starts and ends separately and sweep with two pointers, since only the count of open meetings matters. See `heap-patterns`.
- Intersect two sorted lists, `interval-list-intersections`: no sort. `lo = max(starts)`, `hi = min(ends)`; if `lo <= hi` append `[lo, hi]`. Then advance `i` when `firstList[i][1] < secondList[j][1]`, else `j`. One pass, O(m + n).
- Stab all intervals with the fewest points, `minimum-number-of-arrows-to-burst-balloons`: sort by end, as in `non-overlapping-intervals`. Shoot at the first balloon's end (`arrow_x = end`); every later balloon with `start <= arrow_x` is already hit. A balloon with `start > arrow_x` needs a new arrow. Touching counts as hit, the opposite of the removal count in `non-overlapping-intervals`, where touching is fine to keep.
- Offline queries against intervals, `minimum-interval-to-include-each-query`: sort `intervals` by start and the queries in increasing order. For each `q`, push `(right - left + 1, right)` for every interval with `left <= q`, drop heap tops with end `< q`, and read the size at `heap[0][0]`, else `-1`. Sorted queries mean the started set only grows and an expired interval stays expired. See `heap-patterns`.

## Worked example

Problem: `non-overlapping-intervals`

Sorting by end, then one pass keeping the interval that finishes earliest.

```python
class Solution:

    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda i: i[1])
        removed = 0
        last_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start >= last_end:
                last_end = end
            else:
                removed += 1
        return removed
```

The sort key is the template's decision point: `i[1]`, the end, because the greedy keeps whichever interval frees the line soonest. `last_end` is the invariant from Setup, initialised from the first interval, which is always kept. The test `start >= last_end` is the touching rule: equality is allowed. When it fails, the current interval ends no earlier than the kept one, so dropping it is never worse, and `removed` counts the drop.
