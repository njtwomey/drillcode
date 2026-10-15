## The idea

Matching a pattern with `*` against a string looks like it needs backtracking: should `a*` take two letters or three? Trying every split is exponential on patterns like `a*a*a*b`.

The way out is to notice that the question "does this prefix of `s` match this prefix of `p`?" repeats over and over. There are only `(m+1) * (n+1)` such pairs, so answer each once and store it in a table. Every answer depends only on a few neighbours that were already filled in.

## Set-up

`dp[i][j]` is `True` when the first `i` characters of `s` match the first `j` characters of `p` as a whole.

- `dp[0][0] = True`: the empty string matches the empty pattern.
- Everything else starts `False`.
- Row `i = 0` is filled by the same loop, because a pattern like `c*a*b*` can match the empty string by using zero copies of everything.

Use `s = "aab"` and `p = "c*a*b"`.

```text
          ""  c  *  a  *  b     (columns j = 0..5)
   ""      T  .  .  .  .  .
   a       .
   aa      .
   aab     .
```

## Step by step

The loop fills row by row. Three rules, on column `j`:

- Plain letter or `.`: `dp[i][j] = dp[i-1][j-1]` if the last characters agree.
- `*`, zero copies: `dp[i][j] = dp[i][j-2]`, dropping the two-character item.
- `*`, one more copy: if `p[j-2]` matches `s[i-1]`, also allow `dp[i-1][j]`. Staying in column `j` lets the star repeat.

```text
          ""  c  *  a  *  b
   ""      T  .  T  .  T  .     c* is zero copies, then a* is zero copies
   a       .  .  .  T  T  .     a matches; a* absorbs one a
   aa      .  .  .  .  T  .     a* absorbs another, from the cell above
   aab     .  .  .  .  .  T     b matches, from dp[2][4]
```

The bottom-right cell is `True`: `c*` takes zero copies, `a*` takes two, `b` takes one.

## Why it works

Every match of `s[:i]` against `p[:j]` ends with either a plain item or a starred item `x*`. For a plain item, the last characters must agree and the prefixes before them must match. For a starred item, either it matched nothing (the prefix before the item matches) or it matched at least one character, in which case removing that last character from `s` leaves a string that must still match the whole of `p[:j]`. Those are exactly the three rules, and each reads cells that come earlier in the fill order.

## Where it goes wrong

Using `dp[i-1][j-2]` for the star's extra copy instead of `dp[i-1][j]`. That would allow only one copy, since it also consumes the star item.

```text
s = "aa", p = "a*"
  correct:  dp[2][2] = dp[1][2]  (still inside the star)  -> True
  wrong:    dp[2][2] = dp[1][0]  (item consumed after one a) -> False
```

Another slip is leaving row 0 unfilled, so `a*b*` fails on the empty string.

## Cost

Time O(m * n): each cell is O(1) work. Space O(m * n) for the table (it could shrink to two rows, but the full table is easier to read).
