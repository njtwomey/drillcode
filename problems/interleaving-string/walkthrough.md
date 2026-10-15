## The idea

`s3` is an interleaving if you can split it between `s1` and `s2` while keeping each string's letters in order. Checking letter by letter greedily fails when both strings offer the same letter: you do not know which one to spend. Trying all choices recursively doubles at every tie.

The way out is to ask a smaller question for every pair of prefixes: can the first `i` letters of `s1` and the first `j` letters of `s2` interleave into the first `i + j` letters of `s3`? Those answers build on each other, so a table solves it.

## Set-up

- First check `m + n == len(s3)`. If the lengths do not add up, return `False` immediately.
- `dp[i][j]` is `True` when `s3[:i + j]` is an interleaving of `s1[:i]` and `s2[:j]`. The table is `(m+1) x (n+1)` because prefixes can be empty.
- `dp[0][0] = True`: nothing interleaves into nothing.
- The first row and first column come from the same rule, using only one string.

```text
s1 = "ab"   s2 = "ac"   s3 = "aacb"

          j=0 ""   j=1 "a"  j=2 "ac"
 i=0 ""     T        .         .
 i=1 "a"    .        .         .
 i=2 "ab"   .        .         .
```

## Step by step

The last letter of `s3[:i + j]` is `ch = s3[i + j - 1]`. It came from `s1` if `dp[i-1][j]` is true and `s1[i-1] == ch`, or from `s2` if `dp[i][j-1]` is true and `s2[j-1] == ch`. Filling row by row:

```text
row i=0:  j=1: ch = s3[0] = 'a', s2[0] = 'a', left is T      -> T
          j=2: ch = s3[1] = 'a', s2[1] = 'c' != 'a'           -> .
row i=1:  j=0: ch = s3[0] = 'a', s1[0] = 'a', above is T      -> T
          j=1: ch = s3[1] = 'a', from s1: above dp[0][1]=T, s1[0]='a' -> T
          j=2: ch = s3[2] = 'c', from s2: left dp[1][1]=T, s2[1]='c'  -> T
row i=2:  j=0: ch = s3[1] = 'a', s1[1] = 'b'                  -> .
          j=1: ch = s3[2] = 'c', s1[1]='b', s2[0]='a'         -> .
          j=2: ch = s3[3] = 'b', from s1: above dp[1][2]=T, s1[1]='b' -> T
```

```text
          ""   a    ac
 ""        T   T    .
 a         T   T    T
 ab        .   .    T      <- dp[m][n] = True
```

The path of True cells from top-left to bottom-right is one valid split: take `a` from `s2`, `a` from `s1`, `c` from `s2`, `b` from `s1`.

## Why it works

Any interleaving of the first `i + j` letters ends with a letter taken from `s1[i-1]` or `s2[j-1]`. Removing it leaves an interleaving of a smaller pair of prefixes, which the table already knows. Checking both sources covers every case, including when the two letters are equal.

## Where it goes wrong

- Skipping the length check. The table would still be filled, but `s3[i + j - 1]` could go out of range for a short `s3`.
- Choosing the source greedily when `s1[i-1] == s2[j-1]`. Both options must be tested with `or`.
- Mixing up the shift: `dp[i][j]` refers to `s1[i-1]`, `s2[j-1]` and `s3[i+j-1]`.

## Cost

Time O(m * n): each cell is constant work. Space O(m * n) for the table; since a row only reads the row above and the cell to its left, it could shrink to O(n).
