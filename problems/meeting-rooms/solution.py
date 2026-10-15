"""Sort by start time; any meeting starting before the previous one ends is a conflict.
Touching intervals (end == next start) are fine.

Time O(n log n), space O(1) beyond the sort.
"""


class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals = sorted(intervals)
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True
