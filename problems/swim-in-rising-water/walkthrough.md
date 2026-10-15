## The idea

You can only step onto a cell once the water is at least as high as it. So the time to finish a path is the highest cell along it, not a sum. The answer is the path from the top-left to the bottom-right whose highest cell is as low as possible.

That is shortest path with a different cost rule: the cost of a path is `max` instead of `+`. Dijkstra still works. Always expand the cheapest frontier cell, and the first time the target comes out of the heap, no other route can have a lower worst cell.

A path might be long and winding but low. The shortest-by-steps path is irrelevant.

## Set-up

- `heap` holds `(cost, r, c)` where `cost` is the highest elevation on the best path found to that cell. It starts with `(grid[0][0], 0, 0)`.
- `visited` is the set of cells already pushed. Invariant: a cell's first push carries its best possible cost.

```text
grid = 0 1 2
       7 8 3
       6 5 4

heap = [(0, 0, 0)]    visited = {(0,0)}
```

## Step by step

Each round pops the smallest cost and pushes unseen neighbours with `max(best, their height)`.

```text
pop (0,0,0)   push (1,0) as 7,  (0,1) as 1     heap: (1,0,1) (7,1,0)
pop (1,0,1)   push (1,1) as 8,  (0,2) as 2     heap: (2,0,2) (7,1,0) (8,1,1)
pop (2,0,2)   push (1,2) as 3                  heap: (3,1,2) (7,1,0) (8,1,1)
pop (3,1,2)   push (2,2) as 4                  heap: (4,2,2) (7,1,0) (8,1,1)
pop (4,2,2)   this is the corner: return 4
```

Here is the path found, with the costs carried along it:

```text
 0 ──▶ 1 ──▶ 2
             │
             ▼
             3
             │
             ▼
             4        highest cell on the path is 4
```

The cells 7, 8, 6 and 5 were never needed. The route through the middle would have cost 8.

## Why it works

Costs along a path never decrease, since `max` can only keep or raise the value. That is the property Dijkstra needs. The cheapest cell on the frontier cannot be improved by going through a more expensive one, so when a cell is pushed from the cheapest popped neighbour, that cost is final. Marking cells visited on push is safe for the same reason.

## Where it goes wrong

Using `best + grid[nr][nc]` would add heights as if each step cost something. The correct update is `max(best, grid[nr][nc])`.

```text
sum:  0 + 1 + 2 + 3 + 4 = 10       a made-up cost
max:  max(0, 1, 2, 3, 4) = 4       the water level needed
```

Remember the start cell's own height counts: if `grid[0][0]` is the largest value, the answer is at least that, which the initial `(grid[0][0], 0, 0)` handles.

## Other approaches

Binary search the water level `t` and run a BFS over cells with height at most `t`. The answer is the smallest `t` where the corner is reachable. It costs O(n^2 log n) too.

## Cost

There are n^2 cells and each is pushed once, and heap operations are O(log n^2). Time is O(n^2 log n), space O(n^2).
