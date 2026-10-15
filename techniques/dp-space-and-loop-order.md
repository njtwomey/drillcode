---
title: Space and loop order
area: Dynamic programming
topics: [Dynamic programming]
problems:
  - climbing-stairs
  - house-robber
  - house-robber-ii
  - partition-equal-subset-sum
  - coin-change
  - combination-sum-iv
  - longest-common-subsequence
  - unique-paths
  - maximum-subarray
  - maximum-product-subarray
  - coin-change-ii
  - target-sum
  - perfect-squares
  - minimum-path-sum
  - triangle
  - burst-balloons
  - longest-palindromic-subsequence
  - min-cost-climbing-stairs
related: [dp-finding-the-state, knapsack-patterns, two-string-dp, grid-dp, greedy-one-pass-invariants]
---
## Reach for it when
- The recurrence is clear but the table is larger than needed: `dp[i]` uses only the last one or two entries, or one row of a grid.
- A knapsack-style problem uses each item at most once, or any number of times.
- The same loops count the wrong thing: combinations when the problem wants ordered sequences, or the reverse.
- The structure is circular, so the first and last items interact.

## Setup
- Rolling variables `prev`, `curr` (plus `nxt` if needed) replace `dp[i-2]`, `dp[i-1]`. Invariant: after step `i`, `curr` is `dp[i]` and `prev` is `dp[i-1]`.
- A 1D array `dp` of length `target + 1`, with `dp[0]` the base case. Invariant: during the loop over items, `dp[s]` describes the items seen so far (0/1 case).
- For 2D string DP, a `(m + 1) x (n + 1)` table with a zero row and column. Invariant: `dp[i][j]` is about `text1[:i]` and `text2[:j]`, so characters are `text1[i - 1]` and `text2[j - 1]`.
- For Kadane-style scans, `curr` (best ending here) and `best` (best anywhere). For products, a `curr_max` and `curr_min` pair.

## Template
A 0/1 subset-sum with the target loop downward, and a sequence count with the target loop outside. Swapping either change alters the answer.

```python
def can_make(nums, target):
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
    return dp[target]


def count_sequences(nums, target):
    dp = [1] + [0] * target
    for t in range(1, target + 1):
        for num in nums:
            if num <= t:
                dp[t] += dp[t - num]
    return dp[target]
```

## What it removes
- The full `dp` array when only the last two values are read (`climbing-stairs`, `house-robber`, `decode-ways`): space drops from O(n) to O(1).
- The item dimension of a knapsack table. Iterating the target downward lets one array stand in for "the items before this one", since `dp[s - num]` is not yet overwritten.
- The second dimension of a grid DP. In `unique-paths`, `row[j] += row[j - 1]` reads the old `row[j]` (above) and the new `row[j - 1]` (left).

## Pitfalls
- Iterating the 0/1 array upward. Symptom: `partition-equal-subset-sum` returns true for `[1, 2, 5]` (target 4), because the 1 is reused four times. Go downward, stopping at `num`.
- Swapping loop order. With the target outer and numbers inner you count ordered sequences, which `combination-sum-iv` wants (`(1, 2)` and `(2, 1)` differ). With the numbers outer you count combinations. The code compiles either way and gives a different count. For `coin-change` (a minimum) either order gives the same answer.
- The circular split in `house-robber-ii`: run the linear DP on `nums[:-1]` and `nums[1:]`. With one house both slices are empty and give 0, so return `nums[0]` first.
- Kadane with the reset outside the `max`. The reset is inside it: `curr = max(num, curr + num)`.
- Products need both max and min ending here, because a negative number swaps them. Using only the max fails on `[-2, 3, -4]`. Including `num` itself as a candidate handles zeros without a special case.
- Row-major order on an interval table. Symptom: `longest-palindromic-subsequence` reads zeros for `dp[i + 1][j - 1]` and returns too small an answer. Order the loops by what each cell reads.
- Reading the rolling variables in the wrong order. `prev, curr = curr, max(curr, prev + num)` assigns both from old values in one statement; two separate lines would not.

## Variants
- Rolling pair: `climbing-stairs` (`prev, curr = curr, prev + curr`), `house-robber` (`max(curr, prev + num)`).
- Circular: `house-robber-ii` calls the same linear pass on two slices.
- 0/1 knapsack, downward: `partition-equal-subset-sum`.
- Unbounded, upward or target-outer: `coin-change` (amounts outer, coins inner, minimum), `combination-sum-iv` (target outer, ordered count).
- Full 2D table: `longest-common-subsequence` keeps the `(m + 1) x (n + 1)` table with zero padding. A one-row version exists but the catalogue solution keeps the table.
- One row for a grid: `unique-paths`; `minimum-path-sum` (virtual start `dp[0] = 0`, rest infinity); `triangle` goes bottom-up on a copy of the last row so the answer is `dp[0]`. More in `grid-dp`.
- Unbounded counting, coins outer: `coin-change-ii` (`for coin in coins`, then `a` upward) counts combinations. Unbounded minimum: `perfect-squares` over `squares`.
- 0/1 counting with a reduction: `target-sum` counts subsets reaching `goal = (total + target) // 2`, downward. See `knapsack-patterns`.
- Fill order set by dependencies, not row-major: `longest-palindromic-subsequence` has `dp[i][j]` read `dp[i + 1][j - 1]`, `dp[i + 1][j]` and `dp[i][j - 1]`, so `i` runs backwards and `j` forwards. `burst-balloons` fills by interval length `gap`, because `dp[l][k]` and `dp[k][r]` are shorter.
- Rolling pair with a min and a top that is not a step: `min-cost-climbing-stairs` starts `prev, curr = cost[0], cost[1]` (each step's own cost, since starting on step 0 or 1 is allowed), then `prev, curr = curr, step_cost + min(prev, curr)` over `cost[2:]`. Both states are the cheapest path that ends standing on a step. The top lies one past the last step and is reachable from either of the last two, so it returns `min(prev, curr)`, not `curr`.
- Kadane: `maximum-subarray`; max and min pair: `maximum-product-subarray`.

## Worked example
Problem: `partition-equal-subset-sum`

The task is 0/1 subset sum for half the total. One boolean array, scanned downward, replaces the items-by-sums table.

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        # Two equal halves need an even total.
        if total % 2:
            return False
        # Reduced to 0/1 knapsack: is there a subset summing to half the total?
        # The other subset then automatically sums to the other half.
        target = total // 2
        # dp[s] means some subset of the numbers seen so far sums to exactly s.
        dp = [False] * (target + 1)
        dp[0] = True  # the empty subset
        for num in nums:
            # Go downward so dp[s - num] still reflects the state BEFORE this num.
            # Going upward would let the same num be reused several times.
            # Stopping at num avoids a negative index.
            for s in range(target, num - 1, -1):
                if dp[s - num]:
                    dp[s] = True
        return dp[target]
```

`dp` is the 1D array and `dp[0] = True` is the base case. The inner `range(target, num - 1, -1)` is the downward direction. `dp[s - num]` is read before it could be overwritten for this `num`, so each number is used once.
