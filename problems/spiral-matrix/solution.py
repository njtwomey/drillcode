"""Spiral Matrix (#54, medium)

Approach: Four boundaries; traverse each edge then shrink the boundary.
Tricks: Re-check top <= bottom and left <= right before the bottom and left edges, or
    single rows and columns are visited twice.
Edge cases:
  - Single row
  - Single column
  - 1x1
  - Non-square

Time O(m·n), space O(1).
"""


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        # The four borders of the not-yet-visited rectangle. Each lap peels off
        # one ring and shrinks the rectangle by one on every side.
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        result = []
        while top <= bottom and left <= right:
            # Top edge, left to right.
            for c in range(left, right + 1):
                result.append(matrix[top][c])
            top += 1
            # Right edge, downward (starts below the corner we already took).
            for r in range(top, bottom + 1):
                result.append(matrix[r][right])
            right -= 1
            # After shrinking, the rectangle may be empty (it was a single row or
            # column). Re-check, or we would walk the same cells a second time.
            if top <= bottom:
                # Bottom edge, right to left.
                for c in range(right, left - 1, -1):
                    result.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                # Left edge, upward.
                for r in range(bottom, top - 1, -1):
                    result.append(matrix[r][left])
                left += 1
        return result
