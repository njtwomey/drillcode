---
title: Grid traversal
area: Graphs
topics: [Graph, Matrix]
problems:
  - number-of-islands
  - flood-fill
  - pacific-atlantic-water-flow
  - rotting-oranges
  - word-search
  - word-search-ii
  - max-area-of-island
  - surrounded-regions
related: [bfs-shortest-paths, backtracking-template, trie-patterns, graph-building-and-dfs]
---
## Reach for it when
- The input is a 2D grid and the question is about islands, regions, fills, flow or paths.
- Cells connect to their four neighbours (sometimes eight) and the answer depends on which cells are connected.
- You are asked which cells can reach a target such as an ocean or an exit.
- A word or path must be traced through adjacent cells without reusing one.

## Setup
- `rows, cols = len(grid), len(grid[0])`: the bounds. They never change.
- The in-bounds test `0 <= nr < rows and 0 <= nc < cols`, written before the grid is indexed. It keeps every neighbour inside the grid.
- The four neighbours, written inline as `((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))` in the solutions, or as a `DIRS` tuple of offsets. Neighbours are computed, never stored.
- Visited marking: write into the grid when you may modify it (`"1"` to `"0"`, or the new colour). Otherwise use `seen`, a set of `(r, c)`. A cell is marked when it is pushed, so it is pushed at most once.
- `stack = [(r, c)]` for the current search. An explicit stack avoids Python's recursion limit.
- An outer loop over every cell as a possible start, with `count` for the number of starts that found something new.

## Template
```python
def count_regions(grid):
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
```

## What it removes
- It removes the adjacency list. The grid is already the graph, and the neighbours of `(r, c)` follow from arithmetic.
- In-place marking removes the `visited` set.
- Searching backwards from the target removes the search from every cell. Pacific Atlantic runs two searches, one per ocean, instead of one per cell.

## Pitfalls
- Marking a cell when it is popped instead of when it is pushed. The same cell is pushed many times and the work grows badly.
- Flood fill when the new colour equals the old one. The `== old` test keeps matching and the fill never ends, so return early.
- Recursive DFS on a large grid. A grid that is one big island overflows the recursion limit; use a stack or BFS.
- Indexing before the bounds test. Row `-1` wraps around in Python and gives a wrong answer instead of an error.
- Counting diagonal neighbours when the problem says four directions.
- Marking at pop needs a re-check on pop. `surrounded-regions` does this with `board[r][c] != "O"` after popping; without it a duplicate entry is processed twice.
- Word search without restoring the cell after recursing. Later paths see a `"#"` where a letter should be and miss valid words.

## Variants
- Count components: `number-of-islands` sinks each island as it is found and counts the starts.
- Fill from one start: `flood-fill` recolours matching cells. The new colour doubles as the visited marker.
- Reverse search: `pacific-atlantic-water-flow` starts from each ocean's border cells and steps only to cells that are equal or higher. The answer is the intersection of the two reached sets. It uses a `seen` set because heights must not be changed.
- Measure each component: `max-area-of-island` sinks cells as they are pushed, adds one to `area` per pop, and keeps `best = max(best, area)` per start. Its stack avoids recursion limits on one huge island. Diagonal land cells are separate islands because only four neighbours are used.
- Reverse search from the border: `surrounded-regions` seeds `stack` with every border `"O"`, marks reached cells `"S"` and then sweeps once: leftover `"O"` becomes `"X"` and `"S"` goes back to `"O"`. Searching inward from the edge avoids testing each region for escape. It pushes the four neighbours unchecked and tests bounds and `"O"` on pop, so the marker is written at pop, not push. That is correct here, but the stack can hold duplicates.
- Multi-source BFS: `rotting-oranges` seeds the queue with every rotten orange and counts levels. See `bfs-shortest-paths`.
- Backtracking on the grid: `word-search` writes `"#"` into the cell, recurses in four directions and restores the cell. It is recursive and short-circuits with `or`.
- Backtracking guided by a trie: `word-search-ii` only steps to a neighbour that is a child of the current trie node, and deletes exhausted trie branches. See `trie-patterns`.

## Worked example
Problem: `number-of-islands`

Every cell is a possible start. A land cell that is still `"1"` when the loops reach it belongs to an island no earlier flood touched, so it counts once. The flood sinks the cells it visits.

```python
class Solution:

    def numIslands(self, grid: List[List[str]]) -> int:
        rows, cols = (len(grid), len(grid[0]))
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '1':
                    continue
                count += 1
                grid[r][c] = '0'
                stack = [(r, c)]
                while stack:
                    y, x = stack.pop()
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < rows and 0 <= nx < cols and (grid[ny][nx] == '1'):
                            grid[ny][nx] = '0'
                            stack.append((ny, nx))
        return count
```

`rows, cols` and `count` are set before the outer loops. `stack` holds the cells still to expand. The in-place write `grid[ny][nx] = "0"` happens at the same moment as the push, which is the push-time marking the template uses. The solution names the cell `y, x` and the neighbour `ny, nx`.
