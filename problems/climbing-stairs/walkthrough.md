## The idea

To stand on stair `n`, your last move was either a single step from stair `n - 1` or a double step from stair `n - 2`. Those two groups of routes are disjoint and cover everything, so `ways(n) = ways(n - 1) + ways(n - 2)`. That is the Fibonacci rule. A plain recursion recomputes the same values exponentially often, but each value only needs the two before it, so we can roll two variables forward.

## Set-up

- `prev` holds `ways(k - 1)` and `curr` holds `ways(k)` for the current `k`.
- Both start at 1: there is one way to stand at stair 0 (do nothing) and one way to reach stair 1.

So the loop starts with `k = 1`, and it needs `n - 1` rounds to reach `k = n`.

```text
stair k:     0    1    2    3 ...
ways:        1    1    ?    ?
            prev curr
```

## Step by step

For `n = 5` there are four rounds. Each does `prev, curr = curr, prev + curr`.

```text
start     prev=1  curr=1      (ways(0), ways(1))
round 1   prev=1  curr=2      ways(2) = 1 + 1
round 2   prev=2  curr=3      ways(3) = 1 + 2
round 3   prev=3  curr=5      ways(4) = 2 + 3
round 4   prev=5  curr=8      ways(5) = 3 + 5
```

The answer is `curr = 8`. For `n = 1` the loop runs zero times and `curr = 1` is returned, which is correct.

## Why it works

After round `r`, `curr` is `ways(r + 1)` and `prev` is `ways(r)`. The tuple assignment evaluates the right side first, so the new `curr` uses the old values of both. By induction this holds up to `n`.

## Where it goes wrong

Off-by-one on the loop count. Seeding with `ways(0)` and `ways(1)` means `curr` is already `ways(1)`, so you need `n - 1` rounds, not `n`. Running `n` rounds would return `ways(n + 1)`.

Also be careful to assign both variables in one statement. Writing `prev = curr` then `curr = prev + curr` uses the already overwritten `prev` and doubles instead of adding.

## Cost

Time O(n), one addition per round. Space O(1), two integers (no table).
