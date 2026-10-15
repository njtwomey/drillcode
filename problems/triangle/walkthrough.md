## The idea

A path starts at the top and, at each row, steps to one of the two cells directly below. The cheapest path from the top depends on the cheapest paths from the two cells under it, and those depend on the cells under them, and so on. Trying every path is 2^(rows-1) walks. But many walks share the same tail, so the same sub-answers get recomputed again and again.

The fix is to store, for each cell, the cheapest cost of getting from that cell down to the bottom. Then a cell's value is its own number plus the smaller of its two children's stored costs. Start from the bottom row, where the answer is just the cell itself, and work upward. When you reach the apex, you have the answer in one place.

## Set-up

There is one array.

- `dp` is a copy of the last row. `dp[j]` means "cheapest path sum from the cell in column `j` of the row I am processing, down to the bottom".
- The copy (`triangle[-1][:]`) keeps the caller's input untouched.

Going bottom-up has a nice property: row `i` has one more cell than row `i-1`, so cell `j` in row `i` always has children `j` and `j+1` in the row below. No special handling for the ragged edges, and the answer ends up in `dp[0]`.

```text
triangle              dp (bottom row)
      2
     3 4
    6 5 7             index:  0  1  2  3
   4 1 8 3            dp   = [4, 1, 8, 3]
```

## Step by step

For each row `i` from the second-to-last up to row 0, and each column `j` in it, the code does `dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])`.

```text
Row 2 (6 5 7)
  j=0: 6 + min(dp[0]=4, dp[1]=1) = 7
  j=1: 5 + min(dp[1]=1, dp[2]=8) = 6
  j=2: 7 + min(dp[2]=8, dp[3]=3) = 10

  dp = [ 7,  6, 10,  3 ]      last slot is stale, never read again

Row 1 (3 4)
  j=0: 3 + min(dp[0]=7, dp[1]=6)  = 9
  j=1: 4 + min(dp[1]=6, dp[2]=10) = 10

  dp = [ 9, 10, 10,  3 ]

Row 0 (2)
  j=0: 2 + min(dp[0]=9, dp[1]=10) = 11

  dp = [ 11, 10, 10, 3 ]      answer is dp[0] = 11
```

The winning path is 2, 3, 5, 1, which sums to 11.

## Why it works

After processing row `i`, `dp[0..i]` holds the true cheapest-to-bottom cost for every cell of row `i`. Each new value only needs the two cells below, and those were final one row earlier. So by induction, `dp[0]` after row 0 is the cheapest cost from the apex.

Left-to-right order inside a row is safe. Writing `dp[j]` needs the old `dp[j]` and `dp[j + 1]`. The write at `j` only overwrites a slot that has just been consumed, and `dp[j + 1]` has not been touched yet this row.

## Where it goes wrong

Greedy fails. Picking the smaller child at each step can walk you into a huge cell. With `[[1], [2, 3], [100, 100, 1]]` greedy takes 2 and then 100, but the best path is 1, 3, 1 = 5.

```text
      1
     2 3          greedy: 1 -> 2 -> 100 = 103
   100 100 1      best:   1 -> 3 -> 1   = 5
```

The DP never commits early because it looks at full-tail costs, not single cells. Also watch out for forgetting the copy: `dp = triangle[-1]` would overwrite the caller's last row.

## Other approaches

Top-down DP works too, but the first and last cells of each row have only one parent, and the answer is a `min` over the whole last row. Bottom-up avoids both.

## Cost

Time O(n²) for n rows, since there are about n²/2 cells and each is handled once. Space O(n) for `dp`, the width of the last row.
