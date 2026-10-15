"""Meeting Rooms II (#253, medium)

Approach: Sort by start; min-heap of end times; pop when the earliest end is <= the next
    start; answer is the largest heap size.
Tricks: Alternative: sort starts and ends separately and sweep with two pointers.
Edge cases:
  - Touching meetings share a room
  - All meetings overlap

Time O(n log n), space O(n).
"""
import heapq


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # Min-heap of end times of meetings currently holding a room; its size is the
        # number of rooms in use. Processing by start time lets us ask: has the earliest
        # finishing meeting ended by now?
        ends = []
        best = 0
        for start, end in sorted(intervals):
            if ends and ends[0] <= start:  # touching at a boundary does not conflict
                heapq.heapreplace(ends, end)  # reuse that room: swap its end time
            else:
                heapq.heappush(ends, end)  # everyone is busy, so open a new room
            best = max(best, len(ends))
        return best

    # Alternative: sort starts and ends separately and sweep with two pointers.
    def minMeetingRoomsSweep(self, intervals: List[List[int]]) -> int:
        # Rooms needed = peak overlap. Start and end times can be sorted independently
        # because only the count of open meetings matters, not which meeting is which.
        starts = sorted(i[0] for i in intervals)
        ends = sorted(i[1] for i in intervals)
        rooms = 0
        j = 0  # next meeting (by end time) that might have finished
        for s in starts:
            # Some meeting has ended by time s: its room is reused, so count stays flat.
            if s >= ends[j]:
                j += 1
            else:
                rooms += 1  # nothing finished yet, so we need another room
        return rooms
