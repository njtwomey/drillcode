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
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        result = []
        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                result.append(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):
                result.append(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    result.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    result.append(matrix[r][left])
                left += 1
        return result
