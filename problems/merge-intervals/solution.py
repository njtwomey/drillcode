"""Sort by start; extend the last merged interval when the next one overlaps
(next.start <= last.end, taking the larger end), otherwise append it.

Time O(n log n), space O(n).
"""


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        merged = []
        for start, end in sorted(intervals):
            if merged and start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged
