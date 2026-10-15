## The idea

Asking "is this region fully surrounded?" for every `O` region is awkward: you flood each one and track whether it ever touches the edge. Turn the question around. An `O` survives exactly when it is connected (up, down, left, right) to an `O` on the border. So start from the border, mark everything reachable as safe, and flip whatever is left.

That is one flood fill seeded from the border cells, followed by one sweep of the grid.

## Set-up

- `stack` starts with every border cell that holds an `O`. It is the to-do list of a depth-first flood fill.
- The marker `"S"` (safe) written into a cell means two things at once: this cell is connected to the border, and it has been visited. No separate `visited` set is needed.
- Invariant: every `S` is an `O` that is connected to the border.

```text
board                 border O's seed the stack
 X X X X
 X O O X              stack = [(3,1)]
 X X O X
 X O X X
```

## Step by step

Pop `(3,1)`. It is an `O`, so mark it `S` and push its four neighbours. Those are off the grid or `X`, so each is dropped when popped.

```text
after the flood fill:
 X X X X
 X O O X       the O's at (1,1), (1,2), (2,2) were never reached:
 X X O X       no chain of O's links them to a border O
 X S X X
```

The final sweep goes over every cell: any `O` left is enclosed and becomes `X`, and each `S` goes back to `O`.

```text
 X X X X
 X X X X
 X X X X
 X O X X
```

Only the border `O` survived.

## Why it works

The flood fill reaches precisely the `O` cells that have a path of `O`s to the border, because it starts on border `O`s and spreads over `O` neighbours. Anything it did not reach has no such path, so it is surrounded. The sweep is a single translation: unreached `O` to `X`, `S` back to `O`.

## Where it goes wrong

- Connecting diagonally. Only the four straight neighbours count. In the board above, the O at (2,2) and the border O at (3,1) touch only at a corner, so (2,2) is still captured.

```text
      col 1  col 2
row 2   X      O      <- (2,2), enclosed
row 3   O      X      <- (3,1), on the border
        corner contact only, so (2,2) flips to X
```

- Running the search from every `O` and asking "does it reach the border" repeats work and needs a visited set. The border-first direction avoids both.
- Forgetting the restore step leaves `S` characters in the output.
- Small boards (one row or column) have every cell on the border, so nothing is flipped. The seed list handles that without special code.

## Cost

Time O(m·n): each cell is marked at most once, and each marked cell pushes four neighbours. Space O(m·n) for the stack in the worst case.
