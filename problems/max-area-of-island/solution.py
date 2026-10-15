"""Max Area of Island (#695, medium)

Approach: Scan the grid, and from each unvisited land cell flood the island with an
    iterative DFS, counting cells and tracking the maximum.
Tricks: Sink cells as they are pushed so none is counted twice, and use a stack rather
    than recursion for large islands.
Edge cases:
  - No land
  - Diagonal land cells are separate islands
  - Whole grid is one island

Time O(m * n), space O(m * n).
"""

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        best = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 1:
                    continue
                # Found an unvisited island: flood it and count its cells. An explicit
                # stack avoids recursion limits on a grid that is one large island.
                area = 0
                grid[r][c] = 0  # sink cells as they are pushed, so each is counted once
                stack = [(r, c)]
                while stack:
                    cr, cc = stack.pop()
                    area += 1
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                            grid[nr][nc] = 0
                            stack.append((nr, nc))
                best = max(best, area)
        return best
