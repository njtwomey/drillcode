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
related: [heap-patterns, greedy-one-pass-invariants]
---
## Reach for it when

- The input is a list of intervals, meetings, ranges or schedules given as `[start, end]` pairs.
- The question is about overlap: merge, count conflicts, remove the fewest, find a gap, or count how many are active at once.
- Comparing every pair would be O(n^2) and the data can be sorted first.

## Setup

- Sort first. The real decision is the sort key.
  - By start: merging, overlap detection, inserting, and room counting with a heap.
  - By end: the largest set of non-overlapping intervals, equivalently the fewest removals.
- `result = []`: the merged or kept intervals. Invariant: it is sorted and disjoint, so a new interval can only touch `result[-1]`.
- `last_end`: the end of the last kept interval, for the by-end greedy. Invariant: everything kept so far ends at or before it.
- A heap `ends` of end times, for counting rooms. Invariant: it holds the end times of the meetings currently running; its size is the number in use.
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
- Using `<` in the sweep with separate sorted starts and ends when the touching rule says an ending meeting frees its room. Use `s >= ends[j]`.

## Variants

- Merge, `merge-intervals`: the template. Sort by start, extend the last interval or append. Touching counts as overlap.
- Insert into a sorted list, `insert-interval`: no sort, because the input is already sorted and disjoint. One pass, three phases. Copy intervals that end before the new start; absorb every interval that starts at or before the new end by taking `min` of starts and `max` of ends; then emit the new interval and the rest.
- Keep the most, `non-overlapping-intervals`: sort by end, keep an interval when `start >= last_end` and update `last_end`, otherwise count a removal. Touching is fine here.
- Detect any conflict, `meeting-rooms`: sort by start and compare each start with the previous end. Strict `<`, since back-to-back is allowed.
- Count the peak, `meeting-rooms-ii`: sort by start and keep a min-heap of end times; reuse the room whose end is at or before the next start. Or sort starts and ends separately and sweep with two pointers, since only the count of open meetings matters. See `heap-patterns`.

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
