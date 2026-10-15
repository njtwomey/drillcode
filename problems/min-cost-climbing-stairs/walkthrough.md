## The idea

You are on a staircase where leaving step `i` costs `cost[i]`, and you may move one or two steps at a time. The cheapest way to reach any step depends only on the cheapest ways to reach the two steps just below it. That is a tiny dynamic programme: each answer is built from the previous two.

The brute force tries every sequence of one-step and two-step moves, which doubles with every stair. But many sequences end up on the same step, and only the cheapest of them matters. So we keep one number per step instead of a whole path.

## Set-up

Because each step only looks back two places, two variables replace a whole table:

- `prev` is the cheapest total cost of a path that finishes standing on step `i-1`, with that step's own cost already paid.
- `curr` is the same thing for step `i`.

You may start on step 0 or step 1 for free, so before the loop `prev = cost[0]` and `curr = cost[1]`. Each of them is just paying for the step you started on.

```text
cost   [ 1, 100,  1,  1 ]
index    0    1   2   3

prev = 1 (stand on 0)
curr = 100 (stand on 1)
```

## Step by step

For each later step, the cheapest arrival is from the cheaper of the two steps below, plus the step's own cost: `curr = step_cost + min(prev, curr)`, and `prev` slides up to the old `curr`.

```text
start         prev=1    curr=100

step 2 (cost 1)
  came from step 0 (prev=1) or step 1 (curr=100): take 1
  curr = 1 + 1 = 2          prev = 100

step 3 (cost 1)
  came from step 1 (prev=100) or step 2 (curr=2): take 2
  curr = 1 + 2 = 3          prev = 2
```

The top is one position past the last step, and you can hop onto it from step 3 or from step 2. So the answer is `min(prev, curr) = min(2, 3) = 2`. The route is: start on step 0, jump to step 2, jump to the top, paying 1 + 1.

## Why it works

After each round, `curr` is the true minimum cost to stand on step `i`, and `prev` the same for `i-1`. The only ways to land on step `i` are from `i-1` or `i-2`, so taking the smaller of those two (already optimal) and adding the step's own cost is optimal for `i`. By induction, it holds for every step.

## Where it goes wrong

Returning only `curr` is wrong. The last step might be very expensive, and you can skip it by jumping from the step before.

```text
cost [1, 1, 100]
  start: prev=1, curr=1
  step 2: curr = 100 + 1 = 101, prev = 1
  return curr -> 101      (wrong)
  return min(prev, curr) -> 1   (hop from step 1 straight to the top)
```

## Cost

Time O(n): one pass over the costs. Space O(1): two numbers, however many stairs.
