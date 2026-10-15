## The idea

Checking every possible square and testing whether it is all ones is far too slow. Instead, ask for each cell: what is the biggest all-ones square whose bottom-right corner is this cell?

That answer comes straight from three neighbours. A square of side `k` ending here contains squares of side `k - 1` ending at the cell above, the cell to the left, and the cell diagonally up-left. The smallest of those three limits how big this one can be.

## Set-up

- `dp` has one extra row and column of zeros at the top and left. `dp[i][j]` is the side of the best square ending at matrix cell `(i-1, j-1)`.
- The padding means a border cell reads zeros and gets `min(0, 0, 0) + 1 = 1`, with no special case.
- `best` is the largest side seen. The answer is `best * best`, because the problem asks for area.
- Cells are compared to the string `"1"`, since the matrix holds characters.

## Step by step

```text
matrix            padded dp starts as zeros
 1 0 1 1
 1 1 1 1
 0 1 1 1
```

Rows are filled left to right, top to bottom. A `0` cell stays 0.

```text
row 1:  dp = 1 0 1 1
        every 1 has a zero above or to its left, so min(...) + 1 = 1

row 2:  dp = 1 1 1 2
        cell (2,4): min(up 1, left 1, diag 1) + 1 = 2
        cell (2,2): min(up 0, left 1, diag 1) + 1 = 1  (up is 0)

row 3:  dp = 0 1 2 2
        cell (3,3): min(up 1, left 1, diag 1) + 1 = 2
        cell (3,4): min(up 2, left 2, diag 1) + 1 = 2
```

The largest value is 2, so the answer is 4. The cell (3,4) shows the min at work: up and left both allow side 3, but the diagonal only supports side 1, so the result stops at 2.

```text
 neighbourhood of (3,4)      dp[2][3]=1   dp[2][4]=2
                             dp[3][3]=2   dp[3][4]= min(2, 2, 1) + 1 = 2
```

## Why it works

A square of side `k` with its corner here exists exactly when the cell is 1 and the three neighbouring corners each support a square of side `k - 1`. Those three squares overlap to cover the whole larger square. So the largest `k` is one more than the smallest of the three.

## Where it goes wrong

- Returning `best` instead of `best * best` gives the side, not the area.
- `matrix[i - 1][j - 1]` versus `dp[i][j]` is the usual off-by-one from padding.
- Using `max` instead of `min` would accept squares with a hole.

## Cost

Time O(m * n), one constant-time update per cell. Space O(m * n) for `dp`; it could shrink to two rows since only the previous row is read.
