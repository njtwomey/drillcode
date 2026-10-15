## The idea

Splitting into two subsets with equal sums needs an even total. If it has one, each side must sum to half. So the question becomes: is there a subset of the numbers that adds up to `total / 2`? The other subset then automatically gets the other half.

That is a 0/1 knapsack. Trying every subset is exponential. A boolean array over possible sums answers it in O(n * target).

## Set-up

- `total = sum(nums)`. If it is odd, return `False` at once.
- `target = total // 2`.
- `dp[s]` is `True` when some subset of the numbers seen so far sums to exactly `s`. Size `target + 1`.
- `dp[0] = True`: the empty subset sums to zero.

```text
nums = [1, 5, 11, 5]     total = 22     target = 11

sum:    0  1  2  3  4  5  6  7  8  9 10 11
dp:     T  .  .  .  .  .  .  .  .  .  .  .
```

## Step by step

For each `num`, scan `s` downward from `target` to `num` and set `dp[s] = True` if `dp[s - num]` is `True`.

```text
after num = 1     (s=1: dp[0] is T)
sum:    0  1  2  3  4  5  6  7  8  9 10 11
dp:     T  T  .  .  .  .  .  .  .  .  .  .

after num = 5     (s=6: dp[1] T,  s=5: dp[0] T)
sum:    0  1  2  3  4  5  6  7  8  9 10 11
dp:     T  T  .  .  .  T  T  .  .  .  .  .

after num = 11    (s=11: dp[0] T)
sum:    0  1  2  3  4  5  6  7  8  9 10 11
dp:     T  T  .  .  .  T  T  .  .  .  .  T

after num = 5     (s=10: dp[5] T,  s=11 already T via dp[6])
sum:    0  1  2  3  4  5  6  7  8  9 10 11
dp:     T  T  .  .  .  T  T  .  .  .  T  T
```

`dp[11]` is `True`, so the answer is `True` (for example `{11}` and `{1, 5, 5}`).

## Why it works

Before processing `num`, `dp` describes subsets of earlier numbers. A sum `s` becomes reachable with `num` exactly when `s - num` was reachable without it, so we only read `dp[s - num]` values from before this number was added. Scanning downward guarantees those cells have not been updated yet in this round.

## Where it goes wrong

- Scanning upward. Then `dp[s - num]` may have been set by this same number, so the number is used twice. A number could then be counted twice toward the target.
- Skipping the odd-total check, which makes `total // 2` meaningless.
- Letting the inner range go below `num`, which indexes negatively.

```text
nums = [2, 6]   total 8   target 4   (true answer: False)
  upward scan, num = 2:   s=2: dp[0] T -> dp[2] = T
                          s=4: dp[2] T -> dp[4] = T   (2 used twice, wrong)
  downward scan, num = 2: s=4: dp[2] still F -> stays F
                          s=2: dp[0] T -> dp[2] = T
```

## Cost

Time O(n * target), one pass over `dp` per number. Space O(target) for the single array.
