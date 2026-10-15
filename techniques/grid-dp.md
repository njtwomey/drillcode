---
title: Grid DP
area: Dynamic programming
topics: [Dynamic programming, Matrix]
problems:
  - unique-paths
  - minimum-path-sum
  - triangle
  - maximal-square
  - longest-increasing-path-in-a-matrix
related: [dp-space-and-loop-order, dp-finding-the-state, grid-traversal, matrix-tricks]
---
## Reach for it when
- Moves are restricted (only right and down, or down to an adjacent cell), and the question is a count, a minimum or a largest shape.
- A cell's answer depends on a few neighbours already computed.
- The best path or shape ending (or starting) at a cell is what is needed.
- Moves go in all four directions but each step must strictly increase, so there are no cycles. Then a memoised DFS replaces the table.

## Setup
- `rows, cols`: the dimensions.
- `dp`: one value per cell, or one row. `dp[i][j]` is the answer for the cell `(i, j)` (ending there, or starting there for a bottom-up fill). Write the meaning first.
- Base cells: the start cell, or a padded zero row and column so the borders need no special case.
- Order: row-major when cells read up and left; bottom-up when the answer is easiest to collect at the top.
- One row: when a cell reads only the cell above and the cell to its left, `dp[j]` before the update is the above value and `dp[j - 1]` is the new left value.
- Memoised DFS: `memo` keyed by cell, filled by recursion, when the dependency order is not row-major.

## Template
A row-rolling minimum path sum with a virtual start. It was run on a small grid.

```python
def min_path(grid):
    rows, cols = len(grid), len(grid[0])
    inf = float("inf")
    dp = [inf] * cols
    dp[0] = 0
    for i in range(rows):
        for j in range(cols):
            left = dp[j - 1] if j > 0 else inf
            dp[j] = min(dp[j], left) + grid[i][j]
    return dp[cols - 1]


# min_path([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
```

## What it removes
- A second pass over the grid for the first row and column, because infinity (or a zero pad) stands in for out-of-grid neighbours.
- The full table when each row reads only the previous one: space drops from `rows * cols` to `cols`.
- A visited set in a path problem with strictly increasing steps, since the cell graph has no cycles and a memo is enough.

## Pitfalls
- Greedy neighbour choice in `minimum-path-sum`. Taking the cheaper next cell fails when a cheap step leads to an expensive cell.
- Off by one from the padded table. In `maximal-square`, `dp[i][j]` is for `matrix[i - 1][j - 1]`. Reading `matrix[i][j]` raises IndexError at the last row.
- Comparing to the integer 1. The cells of `maximal-square` are the strings `"1"`, so `matrix[i - 1][j - 1] == 1` never matches.
- Returning the side instead of the area. `maximal-square` returns `best * best`.
- Mutating the input. `triangle` copies the last row (`triangle[-1][:]`) so the caller's data is unchanged.
- A top-down `triangle` needs ragged edge handling and a final `min` over the last row. Going bottom-up avoids both.
- A visited set in `longest-increasing-path-in-a-matrix`. It is not needed, and it breaks sharing: the memo already makes each cell computed once.
- Forgetting that the path may start anywhere. The answer is the maximum over every start cell.

## Variants
- Counting, one row: `unique-paths` starts with `row = [1] * n` and applies `row[j] += row[j - 1]`.
- Minimum cost, one row: `minimum-path-sum` uses `dp = [inf] * cols` with `dp[0] = 0`, so the top-left cost is exactly `grid[0][0]`.
- Bottom-up on a triangle: `triangle` starts with `dp = triangle[-1][:]` and for each higher row sets `dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])`. The answer is `dp[0]`.
- A shape ending at a corner: `maximal-square` has `dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1` on a `"1"`, with a padded zero row and column and `best` as the largest side.
- Memoised DFS: `longest-increasing-path-in-a-matrix` has `memo[(r, c)]` for the longest strictly increasing path starting at `(r, c)`. `dfs` tries four directions into larger values and the answer is the max over all starts.

## Worked example
Problem: `minimum-path-sum`

The state is the cheapest cost to reach a cell, and the row-by-row loop keeps only the current row.

```python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        inf = float("inf")
        dp = [inf] * cols
        dp[0] = 0
        for i in range(rows):
            for j in range(cols):
                left = dp[j - 1] if j > 0 else inf
                dp[j] = min(dp[j], left) + grid[i][j]
        return dp[cols - 1]
```

`dp` is the one row. Before the update, `dp[j]` is the cost from above, and `left` is the cost from the left in this row. `dp[0] = 0` is the virtual start above the top-left cell, so no first-row special case is needed. The answer is the last entry of the final row.
