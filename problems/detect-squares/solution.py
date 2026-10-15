"""Detect Squares (#2013, medium)

Approach: Counter of points; treat each stored point as the diagonal corner and multiply
    the counts of the other two corners.
Tricks: Square means equal non-zero side lengths, so the corners (px, y) and (x, py) are
    forced; multiplying counts handles duplicate points.
Edge cases:
  - Duplicate points multiply the count
  - Query point equal to a stored point (zero area)
  - Rectangle that is not a square
  - Squares on both sides of the query

Time O(1) add, O(p) count (p distinct points), space O(p).
"""

# Judge notes:
# Your DetectSquares object will be instantiated and called as such:
# obj = DetectSquares()
# obj.add(point)
# param_1 = obj.count(point)


from collections import Counter


class DetectSquares:
    def __init__(self):
        # Duplicates are allowed and each copy forms its own square, so keep counts.
        self.points = Counter()

    def add(self, point: List[int]) -> None:
        self.points[(point[0], point[1])] += 1

    def count(self, point: List[int]) -> int:
        x, y = point
        result = 0
        # Treat every stored point as the corner diagonal to the query. A square
        # needs equal, non-zero side lengths; the other two corners are then fixed
        # at (px, y) and (x, py), and the number of squares multiplies the copies.
        for (px, py), diag in self.points.items():
            if abs(px - x) != abs(py - y) or px == x:
                continue
            result += diag * self.points[(px, y)] * self.points[(x, py)]
        return result
