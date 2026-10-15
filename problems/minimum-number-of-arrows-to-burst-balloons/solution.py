"""Minimum Number of Arrows to Burst Balloons (#452, medium)

Approach: Sort by right edge, shoot at the first balloon's end, and skip every balloon
    starting at or before it.
Tricks: Sort by end, not start, and use a strict > so touching balloons share an arrow;
    compare rather than subtract.
Edge cases:
  - Touching balloons share an arrow
  - Nested balloons
  - Endpoints at the 32-bit integer extremes

Time O(n log n), space O(1).
"""

class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        # Greedy on the earliest right edge. Sorted by end, the first balloon must be
        # popped by some arrow, and shooting at its end x is at least as good as any
        # other x inside it: every balloon that starts at or before x and ends after
        # it is hit, and moving left can only lose balloons that begin after the new x.
        # Then skip every balloon that arrow already covers and repeat.
        points.sort(key=lambda p: p[1])
        arrows = 0
        arrow_x = None  # position of the latest arrow
        for start, end in points:
            # A balloon starting exactly at arrow_x is touched, so it shares the arrow
            # (strict > here).
            if arrow_x is None or start > arrow_x:
                arrows += 1
                arrow_x = end
        return arrows
