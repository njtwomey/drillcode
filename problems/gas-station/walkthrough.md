## The idea

Stations sit on a circle. At station `i` you gain `gas[i]` and pay `cost[i]` to reach the next one. We want a starting station from which the tank never goes negative for a full lap.

Trying every start costs O(n^2). Two facts collapse it into one pass.

- If the whole circle has a deficit (total gas less than total cost), no start works.
- If you start at `start` and your tank first goes negative on reaching `i`, then no station between `start` and `i` can be a valid start either. So jump the start to `i + 1`.

## Set-up

- `gain = gas[i] - cost[i]` is the net fuel at station `i`.
- `total` is the sum of every gain. It answers the whole-circle question.
- `tank` is the fuel since the current candidate `start`.
- `start` is the current candidate and begins at 0.

Invariant: `tank` is the fuel on arrival at `i + 1` if we began at `start` and never ran out. The moment it drops below zero the candidate is dead.

```text
gas  = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]
gain = [-2, -2, -2, 3, 3]
index    0   1   2  3  4
```

## Step by step

```text
i   gain   total   tank    start
0    -2     -2      -2 -> reset to 0, start = 1
1    -2     -4      -2 -> reset to 0, start = 2
2    -2     -6      -2 -> reset to 0, start = 3
3    +3     -3       3      start = 3
4    +3      0       6      start = 3

total = 0, which is >= 0, so return start = 3.
```

Checking the answer by driving the lap from station 3:

```text
station 3: tank 0 + 4 - 1 = 3
station 4: tank 3 + 5 - 2 = 6
station 0: tank 6 + 1 - 3 = 4
station 1: tank 4 + 2 - 4 = 2
station 2: tank 2 + 3 - 5 = 0   back at 3, never negative
```

## Why it works

Suppose a start `s` fails at `i`. Any station `k` between `s` and `i` was reached from `s` with a tank of at least 0, so starting fresh at `k` gives no more fuel than starting at `s` did when it got to `k`. So `k` also fails by `i`. Skipping the whole stretch is safe.

At the end, the stretch from `start` to the end of the array never went negative. The part before `start` has some net deficit, but `total >= 0` means the surplus from `start` onward covers that deficit, so the wrap-around part also stays non-negative.

## Where it goes wrong

Resetting `tank` but not `start`, or the other way around. Both change together when the tank goes negative.

Returning `start` without checking `total`. For `gas = [2]`, `cost = [3]`, `start` ends as 1, which is not even a valid index, and the circle can never work.

## Cost

Time O(n): a single pass. Space O(1): four integers.
