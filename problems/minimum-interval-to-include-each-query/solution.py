"""Minimum Interval to Include Each Query (#1851, hard)

Approach: Sort intervals and queries, sweep queries upward pushing started intervals
    onto a min-heap keyed on size, and pop expired ones.
Tricks: Answer queries in sorted order but store results by original index; an expired
    interval stays expired, so lazy popping from the top is enough.
Edge cases:
  - Query covered by no interval returns -1
  - Unsorted queries with duplicates
  - A smaller interval that has already ended

Time O((n + q) log(n + q)), space O(n + q).
"""

import heapq


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # Offline sweep: answer queries in increasing order so the set of intervals
        # that have started only ever grows, then write each answer back at the
        # query's original index (queries may be unsorted and repeated).
        intervals.sort()
        result = [-1] * len(queries)
        heap = []  # (size, end) of every started interval, smallest size on top
        i = 0
        for q, idx in sorted((q, idx) for idx, q in enumerate(queries)):
            # Admit every interval that starts at or before q.
            while i < len(intervals) and intervals[i][0] <= q:
                left, right = intervals[i]
                heapq.heappush(heap, (right - left + 1, right))
                i += 1
            # Lazily drop intervals that end before q. Queries only increase, so an
            # interval that is expired now is expired for every later query too; ones
            # buried below the top are cleaned up when they surface.
            while heap and heap[0][1] < q:
                heapq.heappop(heap)
            if heap:
                result[idx] = heap[0][0]
        return result
