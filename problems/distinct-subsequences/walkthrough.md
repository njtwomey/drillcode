## The idea

Count the number of ways to pick characters from `s`, keeping their order, that spell `t`. Different positions count as different ways, even if they produce the same letters.

Consider the last character of the source prefix, `s[i-1]`, and the last character of the target prefix, `t[j-1]`. There are always the ways that never use `s[i-1]`: that is the count for one shorter source. If the two characters match, there are additionally the ways that do use it as the final letter of `t[:j]`, which leaves the shorter target to be spelled from the shorter source. Add the two groups.

Brute force would enumerate every subset of `s`. The table reuses each smaller answer.

## Set-up

- `dp[i][j]` is the number of ways to pick a subsequence of `s[:i]` that spells `t[:j]`.
- Row 0 (empty source): `dp[0][j] = 0` for `j > 0`, since nothing can be spelled. The code leaves it as the default zero.
- Column 0 (empty target): `dp[i][0] = 1` for every `i`, because the empty string can be made in exactly one way, by choosing nothing.
- Row `i` reads only row `i - 1`, so filling row by row is fine.

```text
s = "babgbag"     t = "bag"

          ""  b  a  g
     ""    1  0  0  0
     b     1
     a     1
     g     1
     b     1
     a     1
     g     1
```

## Step by step

Each cell is `dp[i-1][j]`, plus `dp[i-1][j-1]` if `s[i-1] == t[j-1]`. Each row below is labelled by the character of `s` it adds:

```text
              ""  b  a  g
   ""          1  0  0  0
   b (s[0])    1  1  0  0
   a (s[1])    1  1  1  0
   b (s[2])    1  2  1  0
   g (s[3])    1  2  1  1
   b (s[4])    1  3  1  1
   a (s[5])    1  3  4  1
   g (s[6])    1  3  4  5
```

Walk through two cells:

```text
dp[6][2]  s[5]='a' == t[1]='a':  dp[5][2] + dp[5][1] = 1 + 3 = 4
dp[7][3]  s[6]='g' == t[2]='g':  dp[6][3] + dp[6][2] = 1 + 4 = 5
```

The bottom-right cell says there are 5 ways to spell `"bag"` from `"babgbag"`.

## Why it works

Every selection either leaves out `s[i-1]` or includes it. If it is left out, the selection lives entirely in `s[:i-1]` and spells `t[:j]`. If it is included, it can only play the role of the last letter `t[j-1]`, so it needs to match, and the rest must spell `t[:j-1]` from `s[:i-1]`. The two cases are disjoint and cover everything, so the counts add.

## Where it goes wrong

- Missing the column-0 seed. Without `dp[i][0] = 1`, the "use it" branch would add zero for the first letter and every answer would be 0.
- Dropping the "never use it" term when the characters match. For `s = "aaa"`, `t = "aa"` the answer 3 needs both branches.
- Counting distinct strings instead of positions. Here the same string is counted once per choice of positions.
- When `t` is longer than `s`, the table correctly gives 0 with no special case.

## Cost

Time O(m·n) for the m by n cells. Space O(m·n) for the table; keeping only the previous row would reduce it to O(n), if you fill `j` from right to left.
