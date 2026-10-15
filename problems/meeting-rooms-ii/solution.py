"""Sort by start and keep a min-heap of end times. Reuse a room (pop) when the
earliest end is <= the next start; the answer is the largest heap size.

Time O(n log n), space O(n).
"""
import heapq


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        ends = []
        best = 0
        for start, end in sorted(intervals):
            if ends and ends[0] <= start:
                heapq.heapreplace(ends, end)
            else:
                heapq.heappush(ends, end)
            best = max(best, len(ends))
        return best

    # Alternative: sort starts and ends separately and sweep with two pointers.
    def minMeetingRoomsSweep(self, intervals: List[List[int]]) -> int:
        starts = sorted(i[0] for i in intervals)
        ends = sorted(i[1] for i in intervals)
        rooms = 0
        j = 0
        for s in starts:
            if s >= ends[j]:
                j += 1
            else:
                rooms += 1
        return rooms
