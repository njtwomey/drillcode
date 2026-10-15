## The idea

Flood fill is the paint-bucket tool: starting from one pixel, recolour it and every pixel connected to it (up, down, left, right) that shares its original colour. This is a graph traversal on the grid. Cells are nodes, and an edge joins neighbours that have the same old colour. Any traversal (DFS or BFS) works; this solution uses a stack.

## Set-up

- `old` is the colour of the starting pixel, the colour we are replacing.
- `stack` holds cells we have recoloured but whose neighbours we have not checked yet. It starts with `(sr, sc)`.
- No separate visited set: a recoloured cell no longer equals `old`, so the new colour is the visited marker.

Invariant: every cell on the stack, and every cell already processed, has the new colour. A cell with colour `old` has not been reached.

The early return `if old == color` matters: see below.

## Step by step

Image with start `(1, 1)`, new colour `2`, `old = 1` (the corner `.` cells are 0):

```text
start               after pop (1,1)
 1 1 1               1 2 1       push (0,1), (1,0)
 1 2 0               2 2 0
 1 0 1               1 0 1
stack: [(1,1)]      stack: [(0,1), (1,0)]
```

The neighbours are tried in the order down, up, right, left. From `(1,1)`: down `(2,1)` is 0, up `(0,1)` is 1 so it is recoloured and pushed, right `(1,2)` is 0, left `(1,0)` is 1 so it is recoloured and pushed.

```text
pop (1,0)  push (2,0), (0,0)       pop (0,0)   nothing new
 2 2 1                              2 2 1
 2 2 0                              2 2 0
 2 0 1                              2 0 1
stack: [(0,1),(2,0),(0,0)]         stack: [(0,1),(2,0)]

pop (2,0)  nothing new             pop (0,1)  push (0,2)
stack: [(0,1)]                      2 2 2
                                    2 2 0
                                    2 0 1
                                   stack: [(0,2)]
```

Popping `(0,2)` adds nothing, the stack empties, and the result is:

```text
 2 2 2
 2 2 0
 2 0 1
```

The bottom-right `1` is only touching 0s, so it is not connected and stays.

## Why it works

Each time a cell is recoloured it is pushed once, and it can never match `old` again, so no cell is pushed twice. Every connected `old` cell is reachable through a chain of neighbours, and each pushed cell has all its neighbours examined, so the whole region is covered and nothing beyond it.

## Where it goes wrong

If the new colour equals the old one, recolouring changes nothing, so cells still look unvisited. Without the early return, neighbours would keep re-matching and be pushed forever:

```text
old = 1, color = 1:   (0,0) -> (0,1) -> (0,0) -> (0,1) ...  never ends
```

Recolouring on pop instead of on push is a milder trap: a cell can be pushed several times before it is popped, which wastes work.

## Cost

Time O(m * n) for an m by n image: each cell enters the stack at most once and has four neighbours checked. Space O(m * n) for the stack in the worst case (an all-one-colour image).
