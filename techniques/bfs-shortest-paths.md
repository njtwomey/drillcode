---
title: BFS for fewest steps
area: Graphs
topics: [Graph, Matrix, Tree]
problems:
  - rotting-oranges
  - 01-matrix
  - shortest-path-in-binary-matrix
  - word-ladder
  - open-the-lock
  - binary-tree-level-order-traversal
related: [weighted-shortest-paths, grid-traversal, tree-bfs-by-level, graph-building-and-dfs]
---
## Reach for it when
- The question asks for the fewest moves or the shortest path in an unweighted graph.
- The question asks how long until everything is reached, or how far the nearest something is.
- Edges all cost the same. If edges have different weights, BFS is wrong; use `weighted-shortest-paths`.
- The nodes are states (a word, a lock position) and the edges are a single allowed change.
- Several sources spread at the same time.
- Results must be grouped by distance from the start.

## Setup
- `queue = deque(sources)`: every source is seeded before the loop starts, all at distance 0. The queue holds the cells reached in the current level and then the next one.
- A visited mark, set when a cell is enqueued, not when it is dequeued. A cell is never in the queue twice. Rotting oranges reuses the grid (`1` becomes `2`).
- `fresh`, the number of targets not yet reached, counted before the loop. It decides at the end whether everything was reached.
- `minutes` (the distance), starting at 0 and increased once per level.
- `for _ in range(len(queue))` inside the loop. The length is read once, so cells appended during the pass wait for the next level.

## Template
```python
from collections import deque


def spread_time(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    return -1 if fresh else minutes
```

## What it removes
- Level-by-level order removes any need to store a distance per cell. The number of passes of the outer loop is the distance.
- Seeding all sources at once removes a separate search per source and the min over them. The sources spread in parallel, which is what the problem describes.
- The `fresh` count removes a final scan of the grid to look for unreached cells.

## Pitfalls
- Marking on dequeue. The queue fills with duplicates and the work can blow up.
- Seeding one source at a time. The answer is the time of the slowest source, not the sum or a single run.
- Counting the last level. The loop in the solution stops when `fresh` reaches 0, so an empty final level is not counted as a minute. A grid with no fresh oranges returns 0.
- Returning `minutes` without checking `fresh`. A fresh orange walled off from every rotten one must give `-1`.
- Fresh oranges but nothing rotten. The queue is empty, `fresh` is above 0, and the answer is `-1`.
- Forgetting forbidden or missing start states. `open-the-lock` with `"0000"` in `deadends` must give `-1`, not 0, and `word-ladder` without `endWord` in the list gives 0.
- Reading `len(queue)` inside the loop condition. It changes as you append and the levels merge.

## Variants
- Multi-source grid BFS: `rotting-oranges`, shown below.
- Multi-source distances: `01-matrix` seeds `queue` with every 0 and fills `result`, which starts at `-1` and doubles as the visited mark. It has no level loop: each cell stores `result[r][c] + 1` for its neighbour, so the distance lives in the grid.
- Eight directions: `shortest-path-in-binary-matrix` loops `dr` and `dc` over `(-1, 0, 1)` and carries `length` in the queue tuple. It rejects a blocked start or end first and adds to `seen` at enqueue.
- Implicit graph with wildcard buckets: `word-ladder` groups words under patterns such as `h*t` in `buckets`, then BFS on `(word, steps)`. `buckets.pop(...)` empties a pattern after its first use, since all its words are queued by then. It returns 0 if `endWord` is not in the list.
- Implicit graph with forbidden states: `open-the-lock` starts with `seen = set(deadends)`, so dead ends are pre-visited nodes. It returns `-1` at once if `"0000"` is dead, builds neighbours by turning each wheel by `+1` and `-1` modulo 10, and carries `turns` in the tuple.
- Tree level order: `binary-tree-level-order-traversal` has a single source, the root. The same `for _ in range(len(queue))` pass collects one list per level. It needs no visited mark because a tree has no cycles. It guards against an empty tree before building the queue, since `deque([None])` would fail on `node.val`. See `tree-bfs-by-level`.

## Worked example
Problem: `rotting-oranges`

The queue starts with every rotten orange. Each pass of the `while` loop spreads rot one step and costs one minute.

```python
class Solution:

    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = (len(grid), len(grid[0]))
        queue = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1
        minutes = 0
        while queue and fresh:
            minutes += 1
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and (grid[nr][nc] == 1):
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))
        return -1 if fresh else minutes
```

The first double loop seeds `queue` and counts `fresh`. `minutes` is the level counter. The mark `grid[nr][nc] = 2` is set at the moment of the append, and `fresh -= 1` records the reach. The final line checks that everything was reached.
