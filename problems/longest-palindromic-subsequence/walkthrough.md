## The idea

A subsequence may skip characters, so we cannot just expand from a centre. Instead we ask the same small question about every slice of the string: what is the longest palindromic subsequence inside `s[i..j]`? Answers for short slices build the answers for long ones.

Look at the two ends of a slice. If they match, they can wrap the best palindrome found strictly inside, adding 2. If they differ, at most one of them can be used, so we drop one end and take the better result.

## Set-up

- `dp` is an `n x n` table of zeros. `dp[i][j]` is the answer for `s[i..j]` inclusive.
- `dp[i][i] = 1`, since one character is a palindrome.
- A slice with `j < i` is empty and worth 0. The zero-filled table already says so, which is why `dp[i + 1][j - 1]` is safe when `j = i + 1`.
- `i` runs from the end down, `j` runs up from `i + 1`. Each cell reads `dp[i+1][j-1]`, `dp[i+1][j]` and `dp[i][j-1]`, all of which are already filled in that order.

## Step by step

Take `s = "bbab"`. Rows are filled bottom to top, each row left to right.

```text
        j=0  j=1  j=2  j=3
         b    b    a    b
i=3 b    .    .    .    1        dp[3][3] = 1
i=2 a    .    .    1    1        a vs b differ: max(dp[3][3], dp[2][2]) = 1
i=1 b    .    1    1    3        b vs a: max(1, 1) = 1
                                 b == b: dp[2][2] + 2 = 3
i=0 b    1    2    2    3        b == b: dp[1][0] + 2 = 0 + 2 = 2
                                 b vs a: max(dp[1][2], dp[0][1]) = 2
                                 b == b: dp[1][2] + 2 = 3
```

The final table:

```text
        j=0  j=1  j=2  j=3
i=0      1    2    2    3
i=1      .    1    1    3
i=2      .    .    1    1
i=3      .    .    .    1
```

`dp[0][3] = 3`, for example `bab`. The `dp[1][3] = 3` cell worked by wrapping the `a` in `b ... b`.

## Why it works

Either the outer two characters both belong to an optimal palindrome, in which case they must match and the middle is an optimal palindrome for `s[i+1..j-1]`, or at least one of them is unused, in which case the answer is already inside `s[i+1..j]` or `s[i..j-1]`. Those cases cover everything.

## Where it goes wrong

Filling `i` upward would read cells that are still 0 and silently give wrong answers. The loop direction is not cosmetic.

Do not confuse this with the substring version. Here the chosen letters need not be adjacent, which is why dropping one end (the `max` branch) is allowed at all.

## Cost

Time O(n²): one constant-time update per cell. Space O(n²) for the table. Since each row reads only the row below, it could be cut to O(n), but this solution keeps the full table for clarity.
