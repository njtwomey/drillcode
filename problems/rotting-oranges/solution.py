"""Rotting Oranges (#994, medium)

Approach: Multi-source BFS seeded with every rotten orange, counting levels.
Tricks: Seed the queue with all sources before starting; count fresh oranges to detect
    any left unreachable.
Edge cases:
  - No fresh oranges (0)
  - Unreachable fresh orange (-1)
  - Fresh present but nothing rotten

Time O(m·n), space O(m·n).
"""
from collections import deque


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0
        # Seed the queue with ALL rotten oranges at once. They spread in parallel, so
        # BFS levels equal minutes. Starting from one at a time would be wrong.
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1
        minutes = 0
        # Stop as soon as no fresh oranges remain, so we do not count a final empty
        # level as an extra minute.
        while queue and fresh:
            minutes += 1
            # Process exactly one level (the oranges rotten at the start of this
            # minute); the ones added below belong to the next minute.
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2  # mark now so it is not queued again
                        fresh -= 1
                        queue.append((nr, nc))
        # Fresh oranges left over were walled off from every rotten one.
        return -1 if fresh else minutes
