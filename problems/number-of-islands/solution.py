"""Number of Islands (#200, medium)

Approach: For each unvisited land cell, flood the island and count the start.
Tricks: Marking cells in place ('1' to '0') avoids a visited set.
Edge cases:
  - All water
  - All land
  - Diagonal cells are not connected

Time O(m·n), space O(m·n).
"""


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = len(grid), len(grid[0])
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "1":
                    continue
                count += 1
                grid[r][c] = "0"
                stack = [(r, c)]
                while stack:
                    y, x = stack.pop()
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == "1":
                            grid[ny][nx] = "0"
                            stack.append((ny, nx))
        return count
