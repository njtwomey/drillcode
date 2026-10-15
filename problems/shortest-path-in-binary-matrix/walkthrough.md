## The idea

We want the fewest cells on a path from the top-left to the bottom-right through open cells, where a step can go in any of 8 directions. Every step costs the same, whether it is straight or diagonal. When all edges cost the same, breadth-first search finds the shortest route: it explores every cell one step away, then every cell two steps away, and so on, so the first time it reaches the goal is by a shortest path.

Depth-first search could wander down a long path first, and trying all paths is exponential.

## Set-up

- `n` is the side length.
- The early return: if the start or the end is blocked (`1`), no path exists.
- `seen` holds cells already queued. Cells are added when they are put on the queue, not when they are taken off, so no cell is ever queued twice. Invariant: each cell enters the queue at most once.
- `queue` holds `(row, col, length)` triples, where `length` is the number of cells on the path to that cell, counting both ends. The start has length 1.

```text
grid           queue (front on the left)        seen
 0 0 0         [(0,0,1)]                        {(0,0)}
 1 1 0
 1 1 0
```

## Step by step

Each round pops the front, checks for the goal, then tries all 8 neighbours.

```text
Pop (0,0) len 1   neighbours: (0,1) open -> queue len 2
                  (1,0) (1,1) blocked
                  queue: [(0,1,2)]

Pop (0,1) len 2   (0,2) open -> len 3,  (1,2) open (diagonal) -> len 3
                  (1,0) (1,1) blocked,  (0,0) already seen
                  queue: [(0,2,3), (1,2,3)]

Pop (0,2) len 3   (1,2) already seen; (1,1) blocked
                  queue: [(1,2,3)]

Pop (1,2) len 3   (2,2) open -> len 4
                  queue: [(2,2,4)]

Pop (2,2) len 4   this is (n-1, n-1): return 4
```

```text
 [1] [2] [3]      each cell shows its length; the path is
  #   #  [3]      (0,0) (0,1) (1,2) (2,2) = 4 cells.
  #   #  [4]      The (0,1) -> (1,2) diagonal saves a step.
```

If the queue empties before the goal is popped, the goal is unreachable and the answer is `-1`.

## Why it works

The queue holds cells in non-decreasing order of `length`: everything of length `k` is popped before anything of length `k + 1`. A cell is first queued from the earliest popped neighbour, so its recorded `length` is the shortest possible. When the goal comes off the queue, its length is therefore minimal.

## Where it goes wrong

- Marking cells seen when they are popped instead of when queued. A cell can then be queued many times by different neighbours, and the queue blows up.
- Forgetting the up-front check. A blocked start still lets the loop run and might "find" a route that begins on a wall.
- Looping `dr, dc` over `(-1, 0, 1)` includes `(0, 0)`, the cell itself. That is harmless only because the cell is already in `seen`.

```text
grid [[1]]   start blocked -> -1 without ever entering the loop
grid [[0]]   start is the goal -> first pop returns 1
```

## Cost

Time O(n²): each of the n² cells is queued once and examines 8 neighbours. Space O(n²) for `seen` and the queue.
