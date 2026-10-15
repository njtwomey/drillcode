"""For each unvisited land cell, flood the island (iterative DFS) by marking
cells '0' in place, and count the starts. Diagonals are not connected.

Time O(m*n), space O(m*n) for the DFS stack in the worst case.
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
