## The idea

You want the fewest squares that add up to `n`. Greedy ("take the biggest square that fits") feels natural but fails: for 12 it picks 9 + 1 + 1 + 1 (four squares), while 4 + 4 + 4 needs only three.

Instead, ask the same question for every smaller number. To make `i`, pick some square `sq` as the last piece. What is left is `i - sq`, which is a smaller instance of the same problem. Try every square and keep the best. Because smaller answers get reused, this is a table fill, not an exponential search.

## Set-up

- `squares` lists every square up to `n` in ascending order: for 12 it is `[1, 4, 9]`.
- `dp[i]` is the fewest squares that sum to `i`.
- `dp[0] = 0`: the empty sum needs nothing, and every answer builds on it.
- Every other entry starts at infinity, meaning "not found yet". Since 1 is a square, each entry ends up finite.

```text
n = 12, squares = [1, 4, 9]

i   : 0  1  2  3  4  5  6  7  8  9 10 11 12
dp  : 0  inf ...                          inf
```

## Step by step

The loop goes `i` upward, because `dp[i]` reads smaller indexes. For each `i`, try each `sq <= i` and take `min(dp[i], dp[i - sq] + 1)`.

```text
i=5 : sq=1 -> dp[4]+1 = 2    sq=4 -> dp[1]+1 = 2     dp[5] = 2
i=8 : sq=1 -> dp[7]+1 = 5    sq=4 -> dp[4]+1 = 2     dp[8] = 2
i=12: sq=1 -> dp[11]+1 = 4   sq=4 -> dp[8]+1 = 3
      sq=9 -> dp[3]+1 = 4                            dp[12] = 3

i   : 0  1  2  3  4  5  6  7  8  9 10 11 12
dp  : 0  1  2  3  1  2  3  4  2  1  2  3  3
```

The answer is `dp[12] = 3`, from `dp[8] + 1`, and `dp[8]` itself came from `dp[4] + 1`: that is 4 + 4 + 4.

## Why it works

Any best sum for `i` uses some square as one of its terms. Remove that term and the rest is a best sum for a smaller number (otherwise we could improve the whole). Trying every square covers the true last term, so the minimum is exact. The loop `break`s when `sq > i` because the squares are sorted and none of the later ones fit either.

## Where it goes wrong

- The greedy shortcut, as above.
- Leaving `dp[0]` at infinity: then `dp[1] = dp[0] + 1` never becomes finite.
- Looping `i` downward: `dp[i - sq]` would still be unfilled.

## Cost

Time O(n * sqrt(n)): n entries, about sqrt(n) squares each. Space O(n) for `dp`.
