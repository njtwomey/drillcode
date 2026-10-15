---
title: State machines and interval DP
area: Dynamic programming
topics: [Dynamic programming]
problems:
  - best-time-to-buy-and-sell-stock-with-cooldown
  - burst-balloons
  - regular-expression-matching
  - distinct-subsequences
  - string-to-integer-atoi
related: [dp-finding-the-state, dp-space-and-loop-order, two-string-dp, greedy-one-pass-invariants, math-tricks]
---
## Reach for it when
- Each step puts you in one of a few named modes (holding a share, just sold, free to buy), and the rules say which mode may follow which.
- A rule such as a cooldown, a limit on transactions or a "not twice in a row" constraint makes a single `dp[i]` insufficient.
- The input is a sequence and the question is the best total after the last element, with the mode at the end of each step mattering.
- The state is a range `(l, r)` and the natural decision is which element is handled last in that range (`burst-balloons`).
- A pattern with operators like `*` is matched against a string, and each pattern item can take zero, one or many characters (`regular-expression-matching`).
- A scan has phases (spaces, sign, digits) and you must reject what does not fit. That is the same machine without the optimisation (`string-to-integer-atoi`).

## Setup
- List the modes as a diagram in words, then write one rolling variable per mode. For the cooldown stock problem:
  - `rest` (free to buy) stays `rest`, or arrives from `sold` when the cooldown day ends.
  - `held` stays `held`, or arrives from `rest` by buying. It never arrives from `sold`; that is the cooldown.
  - `sold` arrives only from `held`, by selling today.
- Each variable is the best profit of any history that ends the day in that mode. Impossible modes start at `float("-inf")`, the free mode at 0.
- Compute the new values from yesterday's values only. If an update would read a variable already overwritten, save the old value first (`prev_sold`), or order the lines so each reads before it is changed.
- Interval DP: pad the input with sentinels, let `dp[l][r]` cover the elements strictly between `l` and `r`, and loop over interval length so shorter intervals are ready. The decision is the last element `k` handled in the interval, because its neighbours are then fixed at `l` and `r` and the two sides are independent.
- Pattern table: `dp[i][j]` is true when `s[:i]` matches `p[:j]`, with `dp[0][0] = True`. Row 0 is filled by the same loop.
- Answer: the best over the modes that are allowed to end (for the stock, never `held`), or `dp[0][size - 1]`, or `dp[m][n]`.

## Template
A modal scan: three modes, a cooldown after selling. It was run on `[1, 2, 3, 0, 2]` (answer 3) and `[1]` (answer 0).

```python
def best_profit(prices):
    held = float("-inf")
    sold = float("-inf")
    rest = 0
    for price in prices:
        prev_sold = sold
        sold = held + price
        held = max(held, rest - price)
        rest = max(rest, prev_sold)
    return max(sold, rest, 0)
```

## What it removes
- A table indexed by day and by mode. Each mode needs only yesterday's value, so three variables replace it and space is O(1).
- Case analysis over "did I sell yesterday?" written into the loop. The transitions between modes encode it.
- In the interval form, the dependence between the two sides of a split. Choosing the last element rather than the first fixes its neighbours, so the left and right halves are independent subproblems.

## Pitfalls
- Updating in the wrong order. If `held` is overwritten before `sold` reads it, `sold` uses today's `held` and the answer is too high. In `best-time-to-buy-and-sell-stock-with-cooldown`, `sold = held + price` comes first, `rest` reads the saved `prev_sold`.
- Buying from `sold`. That erases the cooldown: on `[1, 2, 3, 0, 2]` it allows a sale on day 2 and a buy on day 3, giving 4 instead of 3. Buying reads `rest` only.
- Starting `held` at 0 instead of negative infinity. That pretends you own a share for free, and `sold` becomes `price` on day one.
- Returning `held`. Ending while holding a share is never better than having sold or rested, so the answer is `max(sold, rest, 0)`.
- Choosing the first balloon in `burst-balloons`. Its neighbours then depend on later choices and the halves are not independent. The last balloon `k` in `(l, r)` scores `vals[l] * vals[k] * vals[r]`.
- Forgetting the sentinels in `burst-balloons`. Without `vals = [1] + nums + [1]` the edge balloons have no neighbours; with an empty input the padded list `[1, 1]` correctly scores 0.
- In `regular-expression-matching`, the star's repeat case reading `dp[i - 1][j - 1]` or `dp[i][j - 1]`. It must stay on column `j` (`dp[i - 1][j]`) or the star cannot repeat. Not filling row 0 fails `s = ""`, `p = "a*b*"`.
- In `string-to-integer-atoi`, `str.isdigit()` accepts characters `int()` cannot parse, and a second sign must produce 0 because the digit phase reads nothing.

## Variants
- Stock with cooldown, `best-time-to-buy-and-sell-stock-with-cooldown`: the template. Modes are `held`, `sold`, `rest`. The diagram in prose: `rest -> held` by buying, `held -> held` by waiting, `held -> sold` by selling, `sold -> rest` the next day, `rest -> rest` by waiting.
- Interval DP, `burst-balloons`: `dp = [[0] * size for _ in range(size)]`, `for gap in range(2, size)`, `for l in range(size - gap)`, `r = l + gap`, and for `k` strictly between, `coins = vals[l] * vals[k] * vals[r] + dp[l][k] + dp[k][r]`. The answer is `dp[0][size - 1]`. Time O(n^3).
- Pattern table, `regular-expression-matching`: for `p[j - 1] == "*"`, `dp[i][j] = dp[i][j - 2]` (zero copies of `p[j - 2]`), then if `i > 0` and `p[j - 2]` is `.` or equals `s[i - 1]`, OR in `dp[i - 1][j]` (one more copy). Otherwise a plain character or `.` copies `dp[i - 1][j - 1]`. Each pattern position is a mode: it either consumes one character and moves on, or is a starred item that loops on itself. The table is that automaton unrolled over the string.
- Match-or-skip count, `distinct-subsequences`: `dp[i][j] = dp[i - 1][j]`, plus `dp[i - 1][j - 1]` when `s[i - 1] == t[j - 1]`, with `dp[i][0] = 1`. Two choices per cell rather than named modes; shown here for comparison and in `two-string-dp`.
- Parsing machine, the non-DP cousin, `string-to-integer-atoi`: `i` advances through four phases: skip spaces, read one optional sign, read digits (`result = result * 10 + (ord(s[i]) - 48)`, stopping once it exceeds `INT_MAX + 1`), then clamp with `max(INT_MIN, min(INT_MAX, sign * result))`. Nothing is optimised; the "state" is only which phase you are in, and no value is maximised.

## Worked example
Problem: `best-time-to-buy-and-sell-stock-with-cooldown`

Three modes, one variable each. A sale today forces a rest tomorrow, so buying reads only the free mode.

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # State machine, one state per "what am I doing at the end of today":
        #   held = best profit while holding a share
        #   sold = best profit on a day we just sold (tomorrow is forced cooldown)
        #   rest = best profit while holding nothing and free to buy
        # Transitions per price:
        #   held <- stay held, or buy from rest (never from sold: that is the cooldown)
        #   sold <- sell the share held yesterday
        #   rest <- stay resting, or arrive from yesterday's sale (cooldown day ends)
        # Base case before day 0: nothing held (impossible, so -infinity) and no profit.
        held = float("-inf")
        sold = float("-inf")
        rest = 0

        for price in prices:
            prev_sold = sold
            # Update order matters: sold reads yesterday's held, held reads yesterday's
            # rest, and rest reads yesterday's sold. Compute in that order, keeping
            # prev_sold aside.
            sold = held + price
            held = max(held, rest - price)
            rest = max(rest, prev_sold)

        # Ending while still holding is never better than having sold or rested.
        return max(sold, rest, 0)
```

This is the template in a class. `held`, `sold` and `rest` are the modes, `prev_sold` is the saved value that lets `rest` read yesterday's sale, and the three updates run in dependency order. `-inf` marks the impossible start, and the answer ignores `held`.
