"""Walls and Gates (#286, medium)

Approach: Multi-source BFS seeded with every gate at once, writing distance + 1 into
    each empty room.
Tricks: Starting from the gates (not each room) makes it one O(mn) pass, and the INF
    check doubles as the visited set.
Edge cases:
  - No gates, so every room stays INF
  - A room walled off from all gates stays INF
  - Grid with only a wall or only a gate

Time O(m·n), space O(m·n).
"""

# Judge notes:
# Do not return anything: modify rooms in place instead.


from collections import deque


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        if not rooms or not rooms[0]:
            return
        rows, cols = len(rooms), len(rooms[0])
        INF = 2147483647
        # Seed the queue with every gate at once. BFS then expands all gates in
        # lock-step, so the first time a room is reached is from its nearest gate.
        queue = deque((r, c) for r in range(rows) for c in range(cols) if rooms[r][c] == 0)
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                # Only an unvisited empty room (still INF) can be improved; walls
                # and rooms already labelled are skipped, which doubles as the
                # visited check.
                if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
                    rooms[nr][nc] = rooms[r][c] + 1
                    queue.append((nr, nc))
