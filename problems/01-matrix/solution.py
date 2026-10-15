"""01 Matrix (#542, medium)

Approach: Multi-source BFS seeded with every 0 at once, so each cell is first reached
    from its nearest zero.
Tricks: Seed the queue with all zeros together rather than searching from each 1; the
    result grid doubles as the visited set.
Edge cases:
  - Single cell
  - Single row or column
  - Matrix of ones with one zero in a corner

Time O(m * n), space O(m * n).
"""

from collections import deque


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        rows, cols = len(mat), len(mat[0])
        # -1 marks "distance not found yet", so it doubles as the visited flag.
        result = [[-1] * cols for _ in range(rows)]
        # Multi-source BFS: start from every 0 at once. The frontier then grows one
        # step per round from all zeros together, so the first time a cell is reached
        # it is by its nearest zero.
        queue = deque()
        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 0:
                    result[r][c] = 0
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and result[nr][nc] == -1:
                    result[nr][nc] = result[r][c] + 1
                    queue.append((nr, nc))
        return result
