## The idea

You may only move right or down, so any cell is entered from exactly two places: the cell above or the cell to the left. The cheapest way to reach a cell is therefore its own cost plus the cheaper of those two. Brute force tries every path, which is exponential. The DP computes each cell once, from cells already computed.

Picking the cheaper neighbour of the next step (greedy) is wrong: a cheap cell can lead into an expensive region. The DP only looks backwards, at costs that are already final.

## Set-up

- `dp[j]` is the cheapest cost to reach column `j` in the row currently being processed. Before a cell is updated, `dp[j]` still holds the value for the row above; after, it holds the new row's value.
- `dp = [inf] * cols`: before the first row nothing can reach any column from above.
- `dp[0] = 0`: a virtual start sitting just above the top-left cell. This lets the top-left cost exactly `grid[0][0]` and removes any special code for the first row and column.
- `left = dp[j - 1] if j > 0 else inf`: the cell to the left, which was already updated this row. At column 0 there is no left.

```text
grid:  1 3 1
       1 5 1
       4 2 1

dp = [0, inf, inf]      (virtual row above the grid)
```

## Step by step

Each cell does `dp[j] = min(dp[j], left) + grid[i][j]`, where `dp[j]` is "from above" and `left` is "from the left".

```text
Row 0:  j=0: min(0, inf)   + 1 = 1
        j=1: min(inf, 1)   + 3 = 4
        j=2: min(inf, 4)   + 1 = 5
        dp = [1, 4, 5]

Row 1:  j=0: min(1, inf)   + 1 = 2
        j=1: min(4, 2)     + 5 = 7
        j=2: min(5, 7)     + 1 = 6
        dp = [2, 7, 6]

Row 2:  j=0: min(2, inf)   + 4 = 6
        j=1: min(7, 6)     + 2 = 8
        j=2: min(6, 8)     + 1 = 7
        dp = [6, 8, 7]
```

The answer is `dp[cols - 1] = 7`, from the path 1 -> 3 -> 1 -> 1 -> 1.

```text
full table (what the single row passed through):

   1  4  5
   2  7  6
   6  8  7
```

## Why it works

Row by row, left to right, `dp[j - 1]` is the current row's value and `dp[j]` is still the previous row's value. Those are exactly the two cells the current cell can be entered from. Both are optimal for their own cells, and the best path to a cell must end by entering from one of them, so taking the smaller is correct.

## Where it goes wrong

- Forgetting the `j > 0` guard makes `dp[-1]` read the last column, the wrong cell.
- Using `0` instead of `inf` for the missing neighbour lets a path "enter" the first row from nowhere for free.
- Iterating columns in an order other than left to right breaks the "already updated" assumption for `left`.

```text
wrong: left = 0 at j=0 in row 1
  min(dp[0]=1, 0) + 1 = 1   (should be 2: you can only come from above)
```

## Cost

Time O(m * n): one constant-time update per cell. Space O(n): a single row of length `cols`, instead of the full table.
