---
title: Finding the state
area: Dynamic programming
topics: [Dynamic programming]
problems:
  - climbing-stairs
  - house-robber
  - decode-ways
  - word-break
  - unique-paths
  - coin-change
  - combination-sum-iv
  - partition-equal-subset-sum
  - longest-common-subsequence
  - longest-increasing-subsequence
  - maximum-subarray
  - maximum-product-subarray
  - house-robber-ii
related: [dp-space-and-loop-order, backtracking-template, greedy-one-pass-invariants]
---
## Reach for it when
- The question asks to count the ways, find a minimum cost, or decide whether something is possible.
- It asks for the longest or shortest subsequence, or the best value over choices.
- Each choice changes what later choices can do.
- A brute-force recursion solves the same subproblem again and again.

## Setup
Answer these in order before writing a loop.
- What is the smallest subproblem? Usually an empty prefix, amount 0, or a 1x1 grid.
- What does `dp[i]` (or `dp[i][j]`) mean? Write it as one sentence. Every later line must be true to that sentence.
- How does `dp[i]` depend on smaller indices? List the last choice made and the state it came from.
- What are the base cases? Seed them first: `dp[0] = 1`, `dp[0] = 0`, `dp[0] = True`.
- Which loop order has every dependency ready? Increasing `i` when it depends on smaller `i`.
- Where is the answer? The last cell, or a max over all cells when the state is "ending at `i`".

Write the recursive version with `functools.lru_cache` first. Convert to a table only when asked or when recursion depth is a problem.

## Template
A memoised recursion. `best(i)` is the answer for the subproblem identified by `i`, built from smaller `i`.

```python
from functools import lru_cache


def solve(items, target):
    @lru_cache(maxsize=None)
    def best(i):
        # best(i): answer for the subproblem described by i alone.
        if i == 0:
            return 0
        result = float("inf")
        for item in items:
            if item <= i:
                result = min(result, best(i - item) + 1)
        return result

    answer = best(target)
    return answer if answer != float("inf") else -1
```

## What it removes
- The exponential blow-up of trying every sequence of choices. There are only as many distinct subproblems as there are states, and each is solved once.
- The need to decide the "right" first move. The recurrence tries every last choice and keeps the best or the sum.

## Pitfalls
- A state that misses something the future depends on. Symptom: right on the examples, wrong when that hidden fact matters. `house-robber-ii` needs the first-house choice, so it runs the linear DP twice rather than adding a flag.
- "Ending at `i`" versus "within the first `i`". When contiguity or extension matters (`maximum-subarray`, `longest-increasing-subsequence`), the state must end at `i`, and the answer is the max over all `i`. Returning `dp[-1]` for `longest-increasing-subsequence` on `[1, 2, 3, 0]` gives 1, not 3.
- Padding off by one. With a zero row and column, `dp[i]` is about `s[:i]`, so the character is `s[i - 1]`. Using `s[i]` raises IndexError or compares the wrong characters.
- Forgetting the base case for the empty prefix, so every state stays at 0 (counting) or at the sentinel (minimising).
- Using `float("inf")` and then returning it. `coin-change` uses `amount + 1` as infinity and maps it to -1 at the end.

## Variants
The state shape follows the input.
- Prefix ending at `i`: `maximum-subarray`, `maximum-product-subarray` (two values: max and min ending here), `longest-increasing-subsequence` (`dp[i]` over earlier `j`, or a `tails` array).
- First `i` items: `house-robber`, `climbing-stairs`.
- An amount or target: `coin-change` (minimum), `combination-sum-iv` (count), `partition-equal-subset-sum` (boolean).
- Two prefixes: `longest-common-subsequence`, `dp[i][j]` over `text1[:i]` and `text2[:j]`.
- A position in a string: `decode-ways` (count), `word-break` (boolean, last word `s[j:i]`).
- A grid cell: `unique-paths`.

## Worked example
Problem: `decode-ways`

The state is the number of prefix decodings, `dp[i]` for `s[:i]`. The last piece is one digit or two, so `dp[i]` comes from `dp[i-1]` and `dp[i-2]`.

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        prev2, prev1 = 0, 1  # ways for prefixes of length i-2 and i-1; empty prefix has 1 way
        for i in range(1, len(s) + 1):
            cur = 0
            # One-digit decode: any digit but '0' stands alone as a letter.
            if s[i - 1] != "0":
                cur += prev1
            # Two-digit decode: 10..26 only. This rejects '0X' (leading zero) and 27+, and
            # lets '10'/'20' work, since their '0' is not usable on its own.
            if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
                cur += prev2
            # Slide the window; only the last two counts are ever needed.
            prev2, prev1 = prev1, cur
        return prev1
```

Here `prev1` and `prev2` are `dp[i-1]` and `dp[i-2]`, so the table is gone. `prev1 = 1` is the base case for the empty prefix. The two `if` branches are the two choices for the last piece, and the answer is the final `prev1`.
