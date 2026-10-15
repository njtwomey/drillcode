## The idea

We want the fewest coins that sum to `amount`. The tempting move is greedy: take the biggest coin that fits, repeat. That fails. With coins `[1, 3, 4]` and amount 6, greedy takes 4+1+1 (three coins) but 3+3 (two coins) is better.

Instead, solve every smaller amount first. The best way to make `a` ends with some last coin `c`, and before that you made `a - c` as cheaply as possible. So `dp[a] = 1 + min(dp[a - c])` over the coins that fit. Fill the table from 1 upward.

## Set-up

- `dp[a]` is the fewest coins that make `a`. `dp[0] = 0`: zero coins make zero.
- Every other slot starts at `amount + 1`, a stand-in for infinity. No real answer can exceed `amount` (all 1-coins), so `amount + 1` is always worse than any real answer, and it avoids using `float("inf")`.
- A slot that still holds `amount + 1` at the end means unreachable.

```text
coins [1, 3, 4], amount 6      sentinel 7

a      0  1  2  3  4  5  6
dp     0  7  7  7  7  7  7
```

## Step by step

For each `a`, try every coin `c <= a` and take `dp[a - c] + 1` if it is better.

```text
a=1   coin 1: dp[0]+1 = 1                       dp[1] = 1
a=2   coin 1: dp[1]+1 = 2                       dp[2] = 2
a=3   coin 1: dp[2]+1 = 3, coin 3: dp[0]+1 = 1  dp[3] = 1
a=4   coin 1: dp[3]+1 = 2, coin 3: dp[1]+1 = 2,
      coin 4: dp[0]+1 = 1                       dp[4] = 1
a=5   coin 1: dp[4]+1 = 2, coin 3: dp[2]+1 = 3,
      coin 4: dp[1]+1 = 2                       dp[5] = 2
a=6   coin 1: dp[5]+1 = 3, coin 3: dp[3]+1 = 2,
      coin 4: dp[2]+1 = 3                       dp[6] = 2

a      0  1  2  3  4  5  6
dp     0  1  2  1  1  2  2
```

`dp[6] = 2` (3 + 3), beating the greedy answer of 3.

## Why it works

Any optimal way to make `a` has a last coin `c`. Removing it leaves an optimal way to make `a - c`, because a cheaper way would make the whole thing cheaper too. Trying every coin as the last covers all possibilities, and smaller amounts are always ready before bigger ones.

## Where it goes wrong

- Forgetting the unreachable case: with coins `[2]` and amount 3, `dp[3]` stays 4, which is greater than `amount`, so return `-1`.
- Not checking `c <= a`: the index `a - c` would go negative and silently read from the end of the list.
- Amount 0 returns 0 straight from `dp[0]`.

## Cost

Time O(amount * coins): for each amount, one check per coin. Space O(amount) for `dp`.
