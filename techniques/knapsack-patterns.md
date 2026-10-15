---
title: Knapsack patterns
area: Dynamic programming
topics: [Dynamic programming]
problems:
  - partition-equal-subset-sum
  - target-sum
  - coin-change
  - coin-change-ii
  - perfect-squares
  - combination-sum-iv
related: [dp-space-and-loop-order, dp-finding-the-state, backtracking-template]
---
## Reach for it when
- A target (an amount, a sum, a count) must be built from items drawn from a list.
- Each item may be used once (0/1) or any number of times (unbounded).
- The question asks whether it is possible, how many ways, or the fewest items.
- A problem hands out plus and minus signs and asks for a total. It is a subset sum in disguise.

## Setup
- `dp`: a list of length `target + 1`. `dp[s]` is the answer for sum `s`. Write the meaning as one sentence, including whether order counts.
- `dp[0]`: the empty selection. `True` for feasibility, `1` for counting, `0` for minimising. Every other cell starts at the neutral value: `False`, `0`, or infinity.
- Loop direction inside the item loop. Downward (`range(target, num - 1, -1)`) lets `dp[s - num]` still describe the state before this item, so each item is used once. Upward lets `dp[s - num]` already include this item, so it can be reused.
- Loop nesting for counting. Items outer, sums inner counts combinations (order ignored). Sums outer, items inner counts ordered sequences.
- For a minimum, nesting does not change the answer. Use infinity (or `amount + 1`) for unreachable and map it back at the end.

## Template
Two counters on one array shape: a 0/1 count (downward) and an unbounded combination count (upward). Both were run on small inputs.

```python
def count_subsets(nums, goal):
    # each number at most once: sums run downward
    dp = [1] + [0] * goal
    for num in nums:
        for s in range(goal, num - 1, -1):
            dp[s] += dp[s - num]
    return dp[goal]


def count_combinations(coins, amount):
    # each coin any number of times: sums run upward, coins outer
    dp = [1] + [0] * amount
    for coin in coins:
        for s in range(coin, amount + 1):
            dp[s] += dp[s - coin]
    return dp[amount]


# count_subsets([1, 1, 2, 3], 4) == 3
# count_combinations([1, 2, 5], 5) == 4
```

## What it removes
- The items dimension of the table. `dp[i][s]` over the first `i` items collapses to one array, because the loop direction decides which version of `dp[s - num]` is read.
- Enumerating subsets or sequences. The array holds one number per sum, so the work is `len(items) * target`.
- Sign bookkeeping. Assigning `+` or `-` to every number reduces to choosing the `+` subset with a known sum.

## Pitfalls
- Wrong direction. Upward in a 0/1 loop reuses an item: `partition-equal-subset-sum` says yes for `[1, 2, 5]`. Downward in an unbounded loop forbids reuse, so `coin-change-ii` with `[1]` and amount 3 gives 0.
- Wrong nesting when counting. `coin-change-ii` with amount 3 and coins `[1, 2]` should give 2 (`1+1+1`, `1+2`). Sums outer gives 3, which is the `combination-sum-iv` answer.
- Not checking the reduction in `target-sum`. The goal is `(total + target) / 2`. Return 0 when `abs(target) > total` or `total + target` is odd. Skipping this indexes a negative or fractional length.
- Zeros in `target-sum`. A `0` can take either sign, so the count must double. The downward loop does this by itself: with `num = 0`, `dp[s] += dp[s]`. Do not filter zeros out.
- `dp[0]` set to `0` when counting. Every cell then stays 0.
- Returning infinity. `perfect-squares` always ends finite because 1 is a square, but `coin-change` can be unreachable and must return -1.
- Greedy largest-first. `perfect-squares` for 12 is 4+4+4, not 9+1+1+1.

## Variants
- Feasibility, 0/1: `partition-equal-subset-sum` asks for a subset with sum `total // 2`, after rejecting an odd total. `dp` is a list of booleans scanned downward.
- Counting, 0/1, via a sign reduction: `target-sum` computes `goal = (total + target) // 2` and counts subsets reaching it, with `dp[s] += dp[s - num]` downward. The `+` numbers sum to `goal`, the `-` numbers to the rest.
- Minimising, unbounded: `coin-change` fills amounts upward with coins inner and `amount + 1` as infinity. `perfect-squares` is the same with `squares = [k * k ...]` as the coins and `dp[0] = 0`, plus an early `break` once `sq > i`.
- Counting combinations, unbounded: `coin-change-ii` has `for coin in coins` outer and `for a in range(coin, amount + 1)` inner.
- Counting ordered sequences: `combination-sum-iv` has `for t in range(1, target + 1)` outer and `nums` inner, so `(1, 2)` and `(2, 1)` both count.
- Recursion over the same choices, without a table, is `backtracking-template`. The table replaces it when only the count or the feasibility is wanted.

## Worked example
Problem: `target-sum`

Signs split `nums` into a `+` group and a `-` group. The `+` group must sum to `(total + target) / 2`, so the task is a 0/1 subset count.

```python
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        if abs(target) > total or (total + target) % 2:
            return 0
        goal = (total + target) // 2
        dp = [0] * (goal + 1)
        dp[0] = 1
        for num in nums:
            for s in range(goal, num - 1, -1):
                dp[s] += dp[s - num]
        return dp[goal]
```

`goal` is the target sum and the early return handles impossible parity. `dp[0] = 1` is the empty subset. The inner `range(goal, num - 1, -1)` is the downward scan that uses each `num` once. With `num = 0` the line becomes `dp[s] += dp[s]`, which doubles the counts.
