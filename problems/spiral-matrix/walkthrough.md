## The idea

Walking a spiral is easy to describe: go right, go down, go left, go up, then repeat on the smaller rectangle inside. The hard part is knowing when to turn and when to stop. Instead of tracking a position and a direction, keep the four borders of the part of the grid not yet visited. Walk along one whole edge, move that border inward by one, and move on to the next edge.

## Set-up

- `top`, `bottom`, `left`, `right` are the inclusive borders of the unvisited rectangle. Invariant: every cell outside them is already in `result`.
- `result` collects the values in spiral order.

```text
matrix (3 x 4)               top=0
   left=0                    bottom=2
   1   2   3   4             left=0
   5   6   7   8             right=3
   9  10  11  12
```

## Step by step

Each lap does four edges: top (left to right), right (downward), bottom (right to left), left (upward). After an edge, its border moves in.

```text
Lap 1
  top edge    1 2 3 4        top    -> 1
  right edge  8 12           right  -> 2     (starts under the corner)
  bottom edge 11 10 9        bottom -> 1
  left edge   5              left   -> 1     (stops above the corner)

   [1  2  3  4]       result so far: 1 2 3 4 8 12 11 10 9 5
   [5] 6  7 [8]
   [9 10 11 12]       unvisited: row 1, columns 1..2  ->  6 7

Lap 2   top=1 bottom=1 left=1 right=2
  top edge    6 7            top    -> 2
  right edge  rows 2..1 is empty, nothing added     right -> 1
  top <= bottom?  2 <= 1 is false, skip the bottom edge
  left <= right?  1 <= 1 is true, but the left edge runs from row
                  bottom=1 up to top=2, which is empty    left -> 2

Loop test: top <= bottom is false. Done.
result: 1 2 3 4 8 12 11 10 9 5 6 7
```

## Why it works

Each edge is walked only over cells inside the current rectangle, and its border shrinks right after, so no cell is ever walked twice and no cell is skipped. The right edge starts at `top + 1` (because `top` has just moved down), and the left edge stops at `top`, so corners belong to exactly one edge. The loop condition ends it when the rectangle has no area left.

## Where it goes wrong

A single row or single column leaves the rectangle empty partway through a lap. Without the re-checks `top <= bottom` and `left <= right` before the bottom and left edges, the code would walk the same cells again.

```text
matrix [[1, 2, 3]]   top=bottom=0, left=0, right=2
top edge: 1 2 3, then top=1, right=1
Without the check, bottom edge (row 0, cols 1..0) adds 2 1 -> wrong
With top <= bottom false (1 <= 0), it is skipped.
```

The same happens for a single column on the left edge.

## Cost

Time O(m·n): every cell is appended once. Space O(1) beyond the output list.
