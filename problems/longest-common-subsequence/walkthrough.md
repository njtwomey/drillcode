## The idea

A subsequence keeps letters in order but may skip some. To compare two strings, look at their last letters. If they match, that letter can be the end of a common subsequence, and the rest is the best for both strings without it. If they differ, at least one of them cannot be used, so drop the last letter of one string or the other and keep the better outcome.

That splits a big question into smaller questions about prefixes. There are only `m * n` distinct prefix pairs, so a table that remembers each answer avoids the exponential blow-up of trying all subsequences.

## Set-up

- `dp[i][j]` is the LCS length of `text1[:i]` and `text2[:j]`.
- The table has an extra row and column of zeros for the empty prefix. An empty string shares nothing, so those are the base cases and no index checks are needed.
- Because of that shift, character `i` of the table is `text1[i - 1]`.

```text
text1 = "abcde"    text2 = "ace"

        ""  a  c  e
  ""     0  0  0  0
  a      0
  b      0
  c      0
  d      0
  e      0
```

## Step by step

Fill row by row. On a match take the diagonal plus 1; otherwise take the larger of the cell above and the cell to the left.

```text
row a:  a=a match  -> dp[0][0]+1 = 1
        a vs c     -> max(above 0, left 1) = 1
        a vs e     -> max(0, 1) = 1
row b:  b vs a/c/e no match, carries forward: 1 1 1
row c:  c vs a     -> max(1, 0) = 1
        c=c match  -> diagonal dp[2][1] = 1, +1 = 2
        c vs e     -> max(above 1, left 2) = 2
row d:  no matches, carries: 1 2 2
row e:  e vs a     -> 1
        e vs c     -> max(2, 1) = 2
        e=e match  -> diagonal dp[4][2] = 2, +1 = 3
```

```text
        ""  a  c  e
  ""     0  0  0  0
  a      0  1  1  1
  b      0  1  1  1
  c      0  1  2  2
  d      0  1  2  2
  e      0  1  2  3     <- dp[m][n] = 3  ("ace")
```

## Why it works

If the last letters match, there is always an optimal common subsequence that uses them as its final letter, so the answer is one more than the best for the shorter prefixes. If they do not match, any common subsequence leaves out the last letter of at least one string, so the best is the larger of the two shorter problems. Every cell only depends on cells filled earlier.

## Where it goes wrong

- Confusing subsequence with substring. A substring must be contiguous, so a mismatch would reset to 0. Here the `else` branch carries values forward instead.
- Off-by-one on the strings: the check is `text1[i - 1] == text2[j - 1]`, not `text1[i]`.
- Writing `dp[i-1][j-1]` in the else branch. A mismatch needs the above and left cells.

## Cost

Time O(m * n): constant work per cell. Space O(m * n); as each row only reads the row above, it could shrink to O(min(m, n)) by keeping two rows.
