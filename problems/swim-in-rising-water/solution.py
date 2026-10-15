"""Swim in Rising Water (#778, hard)

Approach: Dijkstra where a path costs its highest cell, always expanding the cheapest
    frontier cell until the corner is popped.
Tricks: The cost is max(path so far, cell), not a sum, and binary search on the water
    level plus BFS is an equivalent alternative.
Edge cases:
  - Single cell grid
  - Start or end is the highest cell
  - Shortest path is worse than a longer low path

Time O(n² log n), space O(n²).
"""

import heapq


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        # Dijkstra on a "minimax" path: the cost of a path is the highest cell on it,
        # because we must wait until the water reaches that level. Always expanding
        # the cheapest frontier cell means the first time we pop the target, its
        # cost is the smallest possible maximum.
        # (Alternative: binary search the water level t and BFS over cells <= t.)
        n = len(grid)
        heap = [(grid[0][0], 0, 0)]  # (max elevation on the path so far, row, col)
        visited = {(0, 0)}
        while heap:
            best, r, c = heapq.heappop(heap)
            if r == n - 1 and c == n - 1:
                return best
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                    # Marking on push is safe: the neighbour's cost is
                    # max(best, its own height), and the first push comes from the
                    # cheapest popped cell, so no later path can beat it.
                    visited.add((nr, nc))
                    heapq.heappush(heap, (max(best, grid[nr][nc]), nr, nc))
        return -1
