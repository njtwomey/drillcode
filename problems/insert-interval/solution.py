"""Insert Interval (#57, medium)

Approach: Emit intervals ending before the new one; merge every overlapping interval
    into it; emit the rest.
Tricks: Input is already sorted, so one pass suffices.
Edge cases:
  - Insert at the start or end
  - New interval swallows everything
  - Empty list

Time O(n), space O(n).
"""


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        result = []
        start, end = newInterval
        i, n = 0, len(intervals)
        while i < n and intervals[i][1] < start:
            result.append(intervals[i])
            i += 1
        while i < n and intervals[i][0] <= end:
            start = min(start, intervals[i][0])
            end = max(end, intervals[i][1])
            i += 1
        result.append([start, end])
        result.extend(intervals[i:])
        return result
