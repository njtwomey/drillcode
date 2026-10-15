## The idea

This asks how many different bags of coins add up to `amount`. A bag is a multiset, so 1+2 and 2+1 are the same bag. Listing every bag is exponential. Instead, build up the count one coin type at a time.

Let `dp[a]` be the number of bags that sum to `a` using only the coin types processed so far. Adding a new coin type can only add bags that include at least one of that coin, and those are the bags for `a - coin` with one more coin on top.

## Set-up

- `dp` has `amount + 1` slots, all `0`, except `dp[0] = 1`. There is exactly one way to make 0: take nothing. This is also why `amount = 0` returns 1.
- The coins form the outer loop. Each coin type is introduced once, in list order, so a bag is always built in that fixed order and counted once.
- The inner loop over `a` runs upward. A coin may be reused, and going upward means `dp[a - coin]` may already include this very coin.

```text
amount = 5, coins = [1, 2, 5]

a      0  1  2  3  4  5
dp     1  0  0  0  0  0
```

## Step by step

```text
After coin 1:   dp[a] += dp[a-1]  for a = 1..5
a      0  1  2  3  4  5
dp     1  1  1  1  1  1        (only 1+1+...)

After coin 2:   dp[a] += dp[a-2]  for a = 2..5
a      0  1  2  3  4  5
dp     1  1  2  2  3  3        dp[4] = 1 + dp[2] = 1 + 2

After coin 5:   dp[a] += dp[a-5]  for a = 5
a      0  1  2  3  4  5
dp     1  1  2  2  3  4        dp[5] = 3 + dp[0] = 3 + 1
```

The answer is `dp[5] = 4`: 5, 2+2+1, 2+1+1+1, 1+1+1+1+1.

## Why it works

After processing a set of coins, `dp[a]` splits bags into those using none of the newest coin (the old `dp[a]`) and those using at least one (`dp[a - coin]`, which already counts bags with several of that coin because the loop goes upward). Every bag falls in exactly one group.

## Where it goes wrong

Swapping the loops, with amounts outside and coins inside, counts orderings. For `amount = 3`, `coins = [1, 2]` the correct answer is 2 (1+1+1, 1+2). Amount-outer gives 3, because 1+2 and 2+1 are counted separately. That version is Combination Sum IV.

Running the inner loop downward would forbid reuse of a coin, which is the wrong problem (each coin once).

## Cost

Time O(n * amount) for `n` coin types. Space O(amount) for the single `dp` row.
