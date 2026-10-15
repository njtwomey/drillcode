"""Longest Increasing Path in a Matrix (#329, hard)

Approach: DFS from every cell that returns the longest increasing path starting there,
    memoised per cell.
Tricks: Strictly increasing steps make the graph acyclic, so memoisation replaces a
    visited set; try all four directions.
Edge cases:
  - Single cell
  - All values equal (1)
  - Path that turns corners or spirals

Time O(m·n), space O(m·n).
"""

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows, cols = len(matrix), len(matrix[0])
        # memo[(r, c)] = length of the longest strictly increasing path that STARTS at
        # (r, c). Steps must go to a strictly larger value, so a path can never revisit a
        # cell: the cell graph is a DAG and no visited set is needed. The memo makes each
        # cell computed once.
        memo = {}

        def dfs(r: int, c: int) -> int:
            if (r, c) in memo:
                return memo[(r, c)]
            # Base case: with no larger neighbour, the path is the cell alone (length 1).
            best = 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            memo[(r, c)] = best
            return best

        # The path may start anywhere, so try every cell; memo shares the work.
        return max(dfs(r, c) for r in range(rows) for c in range(cols))
