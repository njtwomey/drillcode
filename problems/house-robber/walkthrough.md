## The idea

You cannot rob two neighbouring houses, so at every house there is a choice: skip it, or rob it and give up the previous house. The best total up to house `i` depends only on the best totals up to `i-1` and `i-2`:

best(i) = max(best(i-1), best(i-2) + nums[i])

Trying every subset of non-adjacent houses is exponential. This recurrence solves each prefix once. A greedy rule such as "take the biggest house" fails: in `[2, 1, 1, 2]` the best is the two 2s (4), not any single pick.

## Set-up

Only the last two answers are ever read, so there is no table:

- `curr` is the best haul using houses up to the previous one (index `i-1`).
- `prev` is the best haul using houses up to two back (index `i-2`).

Both start at 0, the haul from no houses.

```text
nums = [2, 7, 9, 3, 1]

 prev = 0    curr = 0
```

## Step by step

Each round runs `prev, curr = curr, max(curr, prev + num)`.

```text
num   skip = curr   rob = prev + num   new prev   new curr
───   ───────────   ────────────────   ────────   ────────
 2         0          0 + 2 = 2           0          2
 7         2          0 + 7 = 7           2          7
 9         7          2 + 9 = 11          7         11
 3        11          7 + 3 = 10         11         11
 1        11         11 + 1 = 12         11         12
```

Reading the 9 row: robbing house 9 means adding it to the best before house 7 (which was 2), giving 11, and that beats skipping it (7). At the 3, robbing gives only 10, so we keep 11. The answer is `curr = 12`, from houses 2, 9 and 1.

## Why it works

After each round `curr` is the true optimum for the houses seen so far, and `prev` is the optimum for one house fewer. The last house is either robbed (then its neighbour is off limits, so we build on the prefix two back) or not (then we inherit the prefix one back). Taking the larger covers both cases.

## Where it goes wrong

The tuple assignment evaluates the right side first, using the old values. Written as two statements it breaks:

```text
curr = max(curr, prev + num)   # curr changed already
prev = curr                    # prev now holds the NEW curr, not the old one
```

Then `prev` and `curr` end up equal and the "two houses back" value is lost. Also remember that a one-house input works because both start at 0.

## Cost

Time O(n): one pass. Space O(1): two numbers instead of an array of n.
