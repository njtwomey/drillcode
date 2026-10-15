## The idea

An island is a group of land cells joined up, down, left or right. To count them, scan the grid. The first time you meet a land cell you have found a new island. Then flood that whole island so none of its other cells can be counted again. Each island is counted exactly once, at the first of its cells the scan reaches.

Flooding by overwriting `"1"` with `"0"` doubles as the visited marker, so no extra set is needed.

## Set-up

- `count`: islands found so far.
- Two nested loops over `r` and `c`. Invariant: every land cell still marked `"1"` at the scan position belongs to an island not yet counted, because earlier floods sank every cell connected to them.
- `stack` holds cells of the current island still to explore. It is an explicit stack (iterative DFS), so a huge single island cannot overflow Python's recursion limit.
- Cells are sunk when pushed, not when popped, so a cell is never queued twice.

```text
grid (. = water, # = land)

   c: 0 1 2 3 4
r0:   # # . . .
r1:   # # . . .
r2:   . . # . .
r3:   . . . # #

count = 0
```

## Step by step

```text
Scan hits (0,0): land, count=1. Sink it, stack=[(0,0)].
  pop (0,0): down (1,0) sink+push, right (0,1) sink+push
  pop (0,1): down (1,1) sink+push
  pop (1,1): neighbours all water or sunk
  pop (1,0): nothing new
  stack empty -> flood done

   c: 0 1 2 3 4
r0:   . . . . .
r1:   . . . . .
r2:   . . # . .
r3:   . . . # #

Scan continues. (0,1)..(1,1) are now water.
Scan hits (2,2): land, count=2. Flood sinks just it.
  its neighbours (2,3), (3,2), (1,2), (2,1) are water: diagonal (3,3) is not a neighbour.

Scan hits (3,3): land, count=3. pop (3,3): right (3,4) sink+push; pop (3,4): done.

   c: 0 1 2 3 4
r0:   . . . . .
r1:   . . . . .
r2:   . . . . .
r3:   . . . . .
```

The answer is `3`.

## Why it works

A flood from a land cell reaches every cell connected to it through side-by-side land, and sinks them all. So when the scan later sees a `"1"`, it cannot be connected to anything already flooded, which means it is a new island. Each cell is pushed at most once and each push does constant work.

## Where it goes wrong

- Including diagonals. The four directions in the loop are only the side neighbours. `[["1","0"],["0","1"]]` has two islands.
- Marking the cell sunk on pop instead of on push. The same cell could then be pushed by two neighbours and processed twice.
- Forgetting the bounds check before reading `grid[ny][nx]`.

```text
1 0
0 1      (0,0) and (1,1) touch only at a corner -> 2 islands, not 1
```

The function also mutates `grid`. Copy it first if the caller needs it intact.

## Cost

Time O(m * n): each cell is visited a constant number of times. Space O(m * n) in the worst case, when the stack holds a large part of a single big island.
