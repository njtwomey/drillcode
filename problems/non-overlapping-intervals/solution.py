"""Non-overlapping Intervals (#435, medium)

Approach: Sort by end; keep an interval only if it starts at or after the last kept end;
    count the rest.
Tricks: Sorting by end, not start, is what makes the greedy choice correct.
Edge cases:
  - Touching intervals do not overlap
  - Single interval

Time O(n log n), space O(1).
"""


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # Greedy: sort by end time. Keeping the interval that finishes earliest leaves the
        # most room for the rest, so the fewest removals equal n minus the max kept.
        intervals.sort(key=lambda i: i[1])
        removed = 0
        # last_end = end of the last interval we chose to keep; the first is always kept.
        last_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start >= last_end:  # no overlap (touching is fine), so keep it
                last_end = end
            else:
                removed += 1  # overlaps the kept one, which ends no later: drop this one
        return removed
