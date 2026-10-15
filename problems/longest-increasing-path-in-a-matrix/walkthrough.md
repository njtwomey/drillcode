## The idea

From any cell you may step to a neighbour with a strictly larger value. Because every step goes up, you can never come back to a cell you have already used. The grid, viewed as a graph of "can step to" arrows, has no cycles. So there is no need to track visited cells on a path.

That also means the longest path starting at a cell never changes depending on how you reached it. It is a fixed number per cell. Compute it once, remember it, and every other path that runs into that cell reuses it. Without the memory, many routes share long tails and the search explodes exponentially.

## Set-up

- `memo[(r, c)]` is the length of the longest strictly increasing path that starts at `(r, c)`.
- `dfs(r, c)` returns it, using the memo if present. Otherwise it starts with `best = 1` (the cell alone) and tries all four neighbours that are in bounds and strictly larger, taking `1 + dfs(neighbour)`.
- The path can start anywhere, so the outer loop calls `dfs` for every cell and takes the maximum.

```text
matrix            arrows go to a strictly larger neighbour

  1   2           1 ──▶ 2
  4   3           │     │
                  ▼     ▼
                  4 ◀── 3
```

## Step by step

Order of the neighbour checks is down, up, right, left. Start with `dfs(0, 0)` (value 1):

```text
dfs(0,0)  value 1
 ├─ down (1,0) value 4 > 1:  dfs(1,0)
 │     no neighbour above 4          -> memo[(1,0)] = 1
 │     candidate 1 + 1 = 2
 └─ right (0,1) value 2 > 1: dfs(0,1)
       down (1,1) value 3 > 2: dfs(1,1)
          left (1,0) value 4 > 3: memo hit, 1
          -> memo[(1,1)] = 2
       candidate for (0,1): 1 + 2 = 3     -> memo[(0,1)] = 3
     candidate 1 + 3 = 4
 -> memo[(0,0)] = 4
```

The remaining calls `dfs(0,1)`, `dfs(1,0)`, `dfs(1,1)` in the outer loop are all memo hits. The maximum is 4, the path 1, 2, 3, 4 that turns a corner.

```text
memo table (longest path starting at each cell)

  4   3
  1   2
```

## Why it works

`memo` holds a true answer for a cell: either 1 (no larger neighbour) or one more than the best neighbour's answer. Strictly increasing steps mean a neighbour's value is bigger, so the recursion always moves toward larger values and must end. Since no cycle exists, each cell is computed once. Trying every cell as a start covers every path.

## Where it goes wrong

- Allowing equal values (`>=`). Then the graph can have cycles, and the recursion would loop forever. With all values equal the answer must be 1.
- Only trying right and down. Paths can go up and left too, as in the example where the best path ends at the bottom-left.
- Forgetting the memo. It still gives the right answer on small grids but takes exponential time on large ones.
- Recursion depth: a long spiral can reach the number of cells deep, which can hit Python's default recursion limit on very large grids.

## Cost

Time O(m·n): each cell computed once, with four neighbour checks. Space O(m·n) for the memo, plus up to O(m·n) recursion depth in the worst case.
