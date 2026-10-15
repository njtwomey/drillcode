"""Shortest Path in Binary Matrix (#1091, medium)

Approach: BFS from the top-left over 8 directions, carrying the path length in the queue
    and marking cells seen when queued.
Tricks: Reject a blocked start or end up front, and mark cells seen at enqueue time so
    none is queued twice.
Edge cases:
  - Blocked start or end cell
  - Single cell grid
  - Start walled in by ones

Time O(n²), space O(n²).
"""

from collections import deque


class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
            return -1
        # BFS finds the fewest-cells path because every move costs the same, whether
        # it is straight or diagonal. Cells are marked seen when queued, so each is
        # queued at most once.
        seen = {(0, 0)}
        queue = deque([(0, 0, 1)])  # row, col, cells on the path so far
        while queue:
            r, c, length = queue.popleft()
            if r == n - 1 and c == n - 1:
                return length
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 \
                            and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        queue.append((nr, nc, length + 1))
        return -1
