## The idea

Putting `+` or `-` in front of every number looks like `2^n` choices. A little algebra turns it into a counting problem. Let `P` be the numbers given `+` and `N` the numbers given `-`. Then:

- `sum(P) - sum(N) = target`
- `sum(P) + sum(N) = total`

Adding the equations gives `sum(P) = (total + target) / 2`. So the question becomes: in how many ways can we pick a subset of `nums` that sums to `goal = (total + target) / 2`? Each such subset is a choice of the `+` numbers, and the rest are `-`. This is the classic 0/1 knapsack, counting version.

If `abs(target) > total`, or `total + target` is odd (so `goal` would not be an integer), no assignment can work and the answer is 0.

## Set-up

- `total = sum(nums)`, `goal = (total + target) // 2`.
- `dp[s]` is the number of subsets of the numbers processed so far that sum to `s`. Invariant: after handling some numbers, `dp` describes subsets of exactly those numbers.
- `dp[0] = 1` at the start: the empty subset makes 0.

```text
nums = [1, 1, 1, 1, 1]   target = 3
total = 5   goal = (5 + 3) / 2 = 4

dp (index = sum):   s:  0  1  2  3  4
                       [1, 0, 0, 0, 0]
```

## Step by step

For each number, update `dp[s] += dp[s - num]` for `s` from `goal` DOWN to `num`. "Take this number" adds the ways to make `s - num` without it.

```text
after 1st 1     s:  0  1  2  3  4
                   [1, 1, 0, 0, 0]
after 2nd 1        [1, 2, 1, 0, 0]
after 3rd 1        [1, 3, 3, 1, 0]
after 4th 1        [1, 4, 6, 4, 1]
after 5th 1        [1, 5, 10, 10, 5]
```

The answer is `dp[4] = 5`: choose which four of the five ones are `+` (five ways), and the last gets `-`, giving 4 - 1 = 3.

## Why it works

Every subset either includes the current number (and then the rest sums to `s - num`) or it does not (and then it already counted in `dp[s]`). So `dp[s]` after the update equals the old `dp[s]` plus the old `dp[s - num]`. Going downward means `dp[s - num]` has not been updated yet in this round, so it still reflects the state before the current number, and each number is used at most once.

## Where it goes wrong

- Looping upward. Then `dp[s - num]` has already been updated this round, so the same number can be counted again, which turns it into the unbounded knapsack.

```text
num = 1, dp = [1, 0, 0]
down: s=2: dp[2] += dp[1]=0;  s=1: dp[1] += dp[0]  -> [1, 1, 0]   (right)
up:   s=1: dp[1] += dp[0];    s=2: dp[2] += dp[1]  -> [1, 1, 1]   (1 used twice)
```

- Skipping the feasibility check. An odd `total + target` makes `goal` fractional, and a target past the total gives a negative `goal`.
- Zeros: each zero can be `+0` or `-0`, so the count doubles. The update `dp[s] += dp[s - 0]` does that, and the range reaches down to `s = 0`.

## Cost

Time O(n · goal): each number sweeps the table. Space O(goal) for the single array.
