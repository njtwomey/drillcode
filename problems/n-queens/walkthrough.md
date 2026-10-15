## The idea

Two queens can never share a row, so every valid board has exactly one queen per row. That turns the problem into: choose a column for row 0, then a column for row 1, and so on. Backtracking does this row by row. If a row has no safe column, undo the previous choice and try the next one.

The only work per placement is checking the column and both diagonals, and a set per line makes that O(1).

## Set-up

- `path[row]` is the column of the queen in that row. It is the board built so far.
- `cols` holds columns already used.
- `diag` holds `row - col` values. All cells on one `\` diagonal share this number.
- `anti` holds `row + col` values. All cells on one `/` diagonal share this number.
- `backtrack(row)` fills rows `row..n-1`. When `row == n`, `path` is a full solution and is turned into strings.

The invariant: the three sets and `path` always describe exactly the queens on rows before `row`.

```text
n = 4, nothing placed

    c0 c1 c2 c3
r0   .  .  .  .       cols = {}  diag = {}  anti = {}
r1   .  .  .  .
r2   .  .  .  .
r3   .  .  .  .
```

## Step by step

Following the search for `n = 4`, starting with column 0 in row 0:

```text
(0,0) Q   cols{0} diag{0} anti{0}
  row 1: c0 same column, c1 diag 0 clash, c2 ok -> (1,2)
    row 2: c0 col, c1 anti 3 clash, c2 col, c3 diag -1 clash   DEAD END
  undo (1,2), try c3 -> (1,3)
    row 2: c0 col, c1 ok -> (2,1)
      row 3: c0 col, c1 col, c2 diag 1 clash, c3 col           DEAD END
    undo (2,1), c2 diag 0 clash, c3 col                        DEAD END
  row 1 exhausted -> undo (0,0)

(0,1) Q   cols{1} diag{-1} anti{1}
  row 1: c3 only safe -> (1,3)
    row 2: c0 ok -> (2,0)
      row 3: c2 ok -> (3,2)   row == 4: solution path = [1,3,0,2]
```

```text
 . Q . .
 . . . Q
 Q . . .
 . . Q .
```

The search then continues with columns 2 and 3 in row 0 and finds the mirror image `[2,0,3,1]`.

## Why it works

Every board with one queen per row is reachable through some sequence of column choices, and a choice is skipped only when it would attack an earlier queen. So nothing valid is pruned and nothing invalid is kept. Undoing the three sets and `path` after each recursive call restores the state to what it was before the choice.

## Where it goes wrong

- Forgetting to remove a value from one of the sets after the call. That leaves a phantom queen, and later branches wrongly reject safe squares.
- Using the same formula for both diagonals. `row - col` and `row + col` identify the two directions; one set cannot do both.
- `n = 2` and `n = 3` simply return an empty list, since every branch dead-ends.

## Cost

Time O(n!) in the worst case: row 0 has n options, but each later row has fewer safe columns. Pruning makes it much faster in practice. Space O(n) for `path`, the sets and the recursion, excluding the output.
