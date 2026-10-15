"""Meeting Rooms (#252, easy)

Approach: Sort by start; check each start is not before the previous end.
Edge cases:
  - Single meeting
  - Touching intervals (end == next start) do not conflict

Time O(n log n), space O(1).
"""


class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals = sorted(intervals)
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False
        return True
