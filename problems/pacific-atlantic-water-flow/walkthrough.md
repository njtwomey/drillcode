## The idea

We want every cell from which water can run downhill (or level) to both oceans. Checking each cell with its own search is O((m*n)^2). Reverse the question instead: start from the ocean and see which cells the ocean can "climb" to. If water goes from a cell down to the coast, then going backwards from the coast we may only step to neighbours that are equal or higher.

Do that once for the Pacific, once for the Atlantic, and keep the cells in both sets.

## Set-up

- `reach(starts)` floods uphill from a list of border cells and returns the set of cells that touch that ocean.
- `seen` starts as the border cells themselves: they touch their own ocean trivially.
- `stack` holds cells to expand. A neighbour is added only if it is in bounds, not yet seen, and `heights[nr][nc] >= heights[r][c]`.
- `pacific` is the top row plus the left column. `atlantic` is the bottom row plus the right column. The ranges skip the shared corner so no cell is listed twice.

```text
heights:
        3 3 3
        3 1 3
        0 2 4

Pacific border (P): top row and left column
Atlantic border (A): bottom row and right column
```

## Step by step

Take the grid above. Pacific starts at `(0,0) (0,1) (0,2) (1,0) (2,0)`; Atlantic starts at `(2,0) (2,1) (2,2) (0,2) (1,2)`.

```text
Pacific flood (uphill from the top row and left column):
  (2,0)=0 -> (2,1)=2 ok (2 >= 0) -> (2,2)=4 ok (4 >= 2)
  (0,2)=3 -> (1,2)=3 ok (3 >= 3)
  (1,1)=1: its neighbours are 3, 3, 3 and 2, and 1 < 2, so no step
           from them is allowed. Never reached.

  P P P          . = not reached
  P . P
  P P P

Atlantic flood (uphill from the bottom row and right column):
  (2,0)=0 -> (1,0)=3 ok -> (0,0)=3 ok -> (0,1)=3 ok
  (1,1)=1 is again never reached.

  A A A
  A . A
  A A A
```

The intersection is every cell except `(1,1)`:

```text
  ✓ ✓ ✓
  ✓ ✗ ✓
  ✓ ✓ ✓
```

The result is the 8 cells sorted, matching the test `[[0,0],[0,1],[0,2],[1,0],[1,2],[2,0],[2,1],[2,2]]`.

## Why it works

A cell can send water to an ocean exactly when there is a non-increasing path from it to that ocean's border. Reverse that path and it is a non-decreasing path from the border to the cell, which is what the flood follows. So `reach(...)` returns exactly the cells that drain to that ocean, and the intersection is the cells that drain to both.

## Where it goes wrong

- Comparing in the wrong direction. Going from the ocean we need `>=`, not `<=`. Flooding downhill finds the cells the ocean could be poured onto, not where water came from.
- Using `>` instead of `>=`. Plateaus of equal height let water move sideways, so `[[1,1],[1,1]]` should return all four cells.
- Starting a search from every cell. It works but is far too slow.

```text
  2 2 2
  2 2 2      with >, the flood cannot step between equal heights, so the
  2 2 2      centre cell (1,1) looks unreachable. It should qualify.
```

## Cost

Time O(m * n): two floods, each cell visited at most once per flood, plus the sort of the answer. Space O(m * n) for the two seen sets.
