## The idea

To turn one word into another with inserts, deletes and replaces, look only at the ends. Suppose we have already worked out the cheapest way to convert every shorter prefix pair. Then converting the current pair needs just one decision about the last characters.

If they match, they cost nothing and we fall back to the pair without them. If they differ, we spend one edit and pick whichever of three options leaves the cheapest remainder. Trying all edit sequences from scratch is exponential. A table of prefix pairs makes it O(m * n).

## Set-up

`dp[i][j]` is the fewest edits to turn the first `i` characters of `word1` into the first `j` characters of `word2`. The table is one larger in each direction so that "zero characters" has a row and a column.

- `dp[i][0] = i`: delete all `i` characters.
- `dp[0][j] = j`: insert all `j` characters.

Because the table has an extra row and column, the characters being compared are `word1[i - 1]` and `word2[j - 1]`.

```text
word1 = "horse"   word2 = "ros"

         ""   r   o   s
   ""     0   1   2   3
   h      1
   o      2
   r      3
   s      4
   e      5
```

## Step by step

Fill row by row. Each cell reads its left, upper and upper-left neighbours, all already filled.

```text
Match:     dp[i][j] = dp[i-1][j-1]
Mismatch:  dp[i][j] = 1 + min(dp[i-1][j-1]   replace
                              dp[i-1][j]     delete from word1
                              dp[i][j-1])    insert into word1
```

Two cells worked through. Cell (h, r) is a mismatch: `1 + min(0, 1, 1) = 1`. Cell (o, o) is a match, so it copies its upper-left neighbour, `dp[1][1] = 1`.

The finished table:

```text
         ""   r   o   s
   ""     0   1   2   3
   h      1   1   2   3
   o      2   2   1   2
   r      3   2   2   2
   s      4   3   3   2
   e      5   4   4   3
```

The answer is `dp[5][3] = 3`. One path: replace `h` with `r`, delete `r`, delete `e` gives `ros`.

## Why it works

The three mismatch options correspond to the three operations on the last character of `word1`. Replace uses up one character from each word. Delete uses up one from `word1` only. Insert uses up one from `word2` only. Each leaves a smaller prefix pair whose best cost is already in the table. Taking the minimum plus one is therefore the best possible.

On a match, never editing the last pair is always at least as good, so the diagonal copy is safe.

## Where it goes wrong

Indexing. With a table of size `(m+1) x (n+1)`, the character for row `i` is `word1[i - 1]`. Using `word1[i]` is off by one and crashes at the last row.

Forgetting the first row and column gives zeros there, so converting to or from the empty string looks free.

## Cost

Time O(m * n): one constant-time cell per pair of prefixes. Space O(m * n) for the table. Keeping only two rows would cut the space to O(n).
