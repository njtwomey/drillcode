"""Search a 2D Matrix (#74, medium)

Approach: Treat the matrix as one sorted array; row = mid // cols, col = mid % cols.
Tricks: One binary search over rows × cols, not two nested ones.
Edge cases:
  - Single row
  - Single column
  - Target below the first element

Time O(log(m·n)), space O(1).
"""


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])
        lo, hi = 0, rows * cols - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            value = matrix[mid // cols][mid % cols]
            if value == target:
                return True
            if value < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return False
