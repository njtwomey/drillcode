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
        intervals.sort(key=lambda i: i[1])
        removed = 0
        last_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start >= last_end:
                last_end = end
            else:
                removed += 1
        return removed
