"""Interval List Intersections (#986, medium)

Approach: Two pointers; the overlap is [max(starts), min(ends)] when valid, then advance
    the interval that ends first.
Tricks: Use lo <= hi so intervals touching at one point count; always advance the
    pointer with the smaller end.
Edge cases:
  - Either list empty
  - Intervals touching at a single point
  - One interval spanning several in the other list

Time O(m + n), space O(1).
"""

class Solution:
    def intervalIntersection(
        self, firstList: List[List[int]], secondList: List[List[int]]
    ) -> List[List[int]]:
        result = []
        i = j = 0
        # Both lists are sorted and internally disjoint, so one pass with two pointers
        # compares every pair that could possibly overlap.
        while i < len(firstList) and j < len(secondList):
            # The overlap, if any, starts at the later start and ends at the earlier end.
            # lo <= hi (not <) keeps single-point overlaps where endpoints touch.
            lo = max(firstList[i][0], secondList[j][0])
            hi = min(firstList[i][1], secondList[j][1])
            if lo <= hi:
                result.append([lo, hi])
            # The interval that ends first cannot overlap anything further along in the
            # other list, so discard it. The other may still reach the next interval.
            if firstList[i][1] < secondList[j][1]:
                i += 1
            else:
                j += 1
        return result
