## The idea

A board is valid if no digit repeats within any row, any column, or any of the nine 3x3 boxes. You do not need to solve anything, only to check what is already placed. The simple way is to remember which digits each unit has seen and fail the moment a digit shows up again. One pass over the 81 cells is enough.

The only fiddly part is naming the boxes. Numbering them 0 to 8 left-to-right, top-to-bottom turns "which box is this cell in" into a formula.

## Set-up

Three lists of nine sets each:

- `rows[r]` holds the digits seen so far in row `r`.
- `cols[c]` holds the digits seen so far in column `c`.
- `boxes[b]` holds the digits seen so far in box `b`.

Invariant: each set contains exactly the digits already scanned in its unit, and none of them repeats (otherwise we would have returned already).

The box index is `b = (r // 3) * 3 + c // 3`. Integer division by 3 gives the band of three rows and the band of three columns; the first is multiplied by 3 to step down a whole box row.

```text
 box numbers          c: 0 1 2   3 4 5   6 7 8
                    r=0  0 0 0   1 1 1   2 2 2
                    r=1  0 0 0   1 1 1   2 2 2
                    r=2  0 0 0   1 1 1   2 2 2
                    r=3  3 3 3   4 4 4   5 5 5
                    ...
                    r=8  6 6 6   7 7 7   8 8 8
```

## Step by step

Take the invalid board whose first rows are:

```text
 r=0:  8 3 . . 7 . . . .
 r=1:  6 . . 1 9 5 . . .
 r=2:  . 9 8 . . . . 6 .
```

Cells are scanned row by row, left to right. Empty cells (`"."`) are skipped.

```text
(0,0) d=8  b=0   all sets empty        add   rows[0]={8}  cols[0]={8}  boxes[0]={8}
(0,1) d=3  b=0                          add   boxes[0]={8,3}
(0,4) d=7  b=1                          add   boxes[1]={7}
(1,0) d=6  b=0                          add   boxes[0]={8,3,6}
(1,3) d=1  b=1  (1,4) d=9  (1,5) d=5    boxes[1]={7,1,9,5}
(2,1) d=9  b=0                          add   boxes[0]={8,3,6,9}
(2,2) d=8  b=0   8 is in boxes[0]       return False
```

The two 8s are in the same box, at (0,0) and (2,2). They are not in the same row or column, so only the box set catches this one. Another 8 further down column 0, at (3,0), would have been caught by `cols[0]` if we had got that far.

## Why it works

Every rule of the puzzle is "no repeat in this unit", and each cell belongs to exactly one row, one column and one box. A repeat in any unit means the second occurrence finds the digit already in that unit's set. If we finish the scan without a hit, no unit has a repeat.

## Where it goes wrong

- Forgetting the box check and only checking rows and columns.
- Writing the box index as `r // 3 + c // 3`. That gives the same value for (0,3) and (3,0), so unrelated cells would share a set.
- Treating `"."` as a digit. Every empty cell would collide with the next one.
- Trying to check solvability. An empty board is valid, and so is a partly filled board that happens to have no solution.

## Cost

Time O(1) and space O(1) in the strict sense, because the board is always 9x9: 81 cells and 27 sets of at most 9 digits. For an n by n board it would be O(n²) for both.
