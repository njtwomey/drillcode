## The idea

A robot walks from the top-left of an m by n grid to the bottom-right, moving only right or down. Every cell can only be entered from the cell above or the cell to its left. So the number of ways to reach a cell is the number of ways to reach the cell above plus the number of ways to reach the cell on the left. That is the whole recurrence.

Counting paths by enumerating them blows up exponentially. Filling in the counts cell by cell takes one visit per cell.

## Set-up

A full m by n table would work, but each row only needs the row before it. So the code keeps just one row.

- `row` has `n` entries, all 1 to start. It is the first grid row: there is exactly one way to reach each top-edge cell, going straight right.
- Column 0 stays 1 forever: there is only one way down the left edge.

While processing a grid row, `row[j]` is still the count for the cell above (old row), and `row[j - 1]` has already been updated to the cell on the left (new row).

```text
m = 3, n = 4

grid row 0:   1  1  1  1        row = [1, 1, 1, 1]
```

## Step by step

For each of the remaining `m - 1` rows, for `j` from 1 to `n - 1`, run `row[j] += row[j - 1]`.

```text
Grid row 1
  j=1: row[1] = 1 + row[0] = 1 + 1 = 2
  j=2: row[2] = 1 + row[1] = 1 + 2 = 3
  j=3: row[3] = 1 + row[2] = 1 + 3 = 4

  row = [1, 2, 3, 4]

Grid row 2
  j=1: row[1] = 2 + row[0] = 2 + 1 = 3
  j=2: row[2] = 3 + row[1] = 3 + 3 = 6
  j=3: row[3] = 4 + row[2] = 4 + 6 = 10

  row = [1, 3, 6, 10]
```

Written as the full grid it would look like this, and the code only ever remembers the latest line:

```text
  1   1   1   1
  1   2   3   4
  1   3   6  10   <- row[-1] = 10
```

## Why it works

Every path to the bottom-right cell has a last step, either from above or from the left. These two groups do not overlap and together cover all paths, so their counts add. The same holds for every cell, by induction from the top row and left column, which have a single path each.

## Where it goes wrong

- Starting the inner loop at `j = 0`. Column 0 has no left neighbour, and `row[-1]` in Python would silently read the last cell.
- Looping `m` times instead of `m - 1`. The first row is already in `row`, so an extra pass would count one row too many.
- With `m = 1` the outer loop does not run, and the answer is `row[-1] = 1`, which is correct. The same goes for `n = 1`.

## Other approaches

Every path has m - 1 downs and n - 1 rights in some order, so the answer is the number of ways to choose positions for the downs: C(m + n - 2, m - 1). For 3 by 4 that is C(5, 2) = 10. It is a one-liner, but the DP is the version that generalises to obstacles.

## Cost

Time O(m·n): one addition per cell. Space O(n): a single row, instead of a full m by n table.
