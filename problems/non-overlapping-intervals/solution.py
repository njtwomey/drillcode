"""Greedy: sort by end, keep an interval only if it starts at or after the last
kept end, and count the rest as removals. Sorting by end makes the choice optimal.

Time O(n log n), space O(1) beyond the sort.
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
