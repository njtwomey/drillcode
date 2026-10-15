"""Merge Intervals (#56, medium)

Approach: Sort by start; extend the last merged interval when the next overlaps,
    otherwise append.
Tricks: Overlap test is next.start <= last.end; take the larger end when merging.
Edge cases:
  - Single interval
  - Touching intervals [1,4] and [4,5]
  - One interval inside another

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
