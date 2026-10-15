## The idea

If a cell is zero, its whole row and column must become zero. The easy fix is to copy the matrix, or to record zero rows and columns in two extra sets. That costs extra memory proportional to the grid or its sides.

The trick is to use space the matrix already has. The first row can store "this column has a zero" and the first column can store "this row has a zero". Those border cells will turn into zeros anyway if the flag is set, so writing a `0` there loses nothing, except for one thing: the borders may have had their own zeros, and those get mixed up with the markers. A pair of booleans taken before any stamping fixes that.

## Set-up

- `first_row` is `True` if the first row had a zero to begin with.
- `first_col` is the same for the first column. Both are saved up front, because afterwards a `0` on a border could be either an original zero or a marker.
- The inner cells (`r >= 1`, `c >= 1`) are the data. The borders are the notepad.

```text
matrix                       first_row = False
  1  1  1                    first_col = False
  1  0  1
  1  1  1
```

## Step by step

Pass 1 scans the inner cells. A zero at `(r, c)` stamps `matrix[r][0] = 0` and `matrix[0][c] = 0`.

```text
Pass 1   inner zero at (1,1): stamp row marker (1,0) and column marker (0,1)

  1  [0]  1        row 0 holds column markers
 [0]  0   1        column 0 holds row markers
  1   1   1
```

Pass 2 revisits only the inner cells: zero any whose row marker or column marker is zero.

```text
Pass 2   (1,1) row marker 0 -> zero      (1,2) row marker 0 -> zero
         (2,1) col marker 0 -> zero      (2,2) neither marker -> stays 1

  1   0   1
  0   0   0
  1   0   1
```

Last, apply the saved flags. Both are `False` here, so the borders keep their markers, which are already the right zeros. The result is the answer.

## Why it works

A marker at `matrix[r][0]` is only ever written because some inner cell in row `r` was zero, and `matrix[0][c]` likewise for column `c`. So reading the markers in pass 2 is exactly the question "does this row or column hold a zero". The borders are zeroed last because they are still needed as readable markers until pass 2 is done.

## Where it goes wrong

- Zeroing the first row or column early. The markers are then wiped and every cell below sees a zero.
- Forgetting to save `first_row` and `first_col` first. A zero that started in the first column would be lost when the markers get overwritten.

```text
  1  2  3        first_col is True (the zero at (1,0) is original).
  0  5  6        Without that flag, the inner pass sees matrix[1][0]=0
  7  8  9        and still zeroes row 1, but column 0 would never be
                 cleared, so the 1 and the 7 would survive.
```

- Starting pass 1 and 2 at index 0, which would read the borders as data.

## Cost

Time O(m·n): a few passes over the grid. Space O(1): two booleans, the borders reuse the matrix.
