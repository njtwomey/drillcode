## The idea

Turning a square 90 degrees clockwise looks like it needs a second grid: the top row becomes the right column, and so on. But the rotation is the same as two simple reflections done one after another, and each reflection is a swap pattern that works in place:

1. Transpose: reflect across the main diagonal, so the cell at row `i`, column `j` swaps with the one at row `j`, column `i`.
2. Reverse every row: mirror left to right.

Transpose followed by reversing rows equals a clockwise quarter turn.

## Set-up

There is not much state, just the size `n = len(matrix)` and the loop indexes.

- In the transpose, `j` starts at `i + 1`. Each pair above the diagonal is swapped once with its partner below it. Starting at `j = 0` would swap every pair twice and undo the work. The diagonal itself stays put.
- In the second step, each `row` is reversed in place.

```text
matrix:        1 2 3
               4 5 6
               7 8 9
```

## Step by step

Step 1, the swaps are (0,1)<->(1,0), (0,2)<->(2,0), (1,2)<->(2,1), that is 2<->4, 3<->7 and 6<->8:

```text
before        after the three swaps

1 2 3          1 4 7
4 5 6    ──▶   2 5 8
7 8 9          3 6 9
```

Step 2, reverse each row:

```text
1 4 7          7 4 1
2 5 8    ──▶   8 5 2
3 6 9          9 6 3
```

The first column `1 4 7` read top to bottom is now the first row read right to left, which is what a clockwise turn does.

## Why it works

After the transpose, the cell that was at `(i, j)` is at `(j, i)`. Reversing the row then sends column `j` to column `n - 1 - j`. So the cell at `(i, j)` ends at `(j, n - 1 - i)`, which is the formula for a clockwise quarter turn.

## Where it goes wrong

- Looping `j` over the whole row in the transpose. Each pair is swapped twice, and the matrix returns to the original.

```text
j from 0:   1 2 3 ──swap all pairs, then swap them back──▶ 1 2 3
```

- Reversing columns instead of rows after the transpose gives a counter-clockwise turn. For clockwise, reverse the rows.
- Rebuilding `matrix = ...` makes a new list and the caller's grid does not change. The task requires in-place edits.

## Cost

Time O(n^2): every cell is touched a constant number of times. Space O(1): only swaps.
