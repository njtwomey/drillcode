## The idea

You do not need to find the path, only to know whether the last index is reachable. Reachable positions always form an unbroken block starting at index 0: if you can reach index 5 you can also reach 3, because a jump of length `n` lets you land anywhere from 1 to `n` steps ahead. So one number describes everything we know: the furthest index reachable so far.

Trying every jump from every index is exponential; a DP over "can I reach index i" is quadratic. The greedy block-edge idea needs one pass.

## Set-up

- `furthest` is the largest index reachable using the positions seen so far. It starts at 0, since we begin at index 0.
- The loop visits each index `i` with its jump length `jump`.

Invariant: every index from 0 to `furthest` is reachable.

```text
nums = [2, 3, 1, 1, 4]

 index:     0  1  2  3  4
 value:     2  3  1  1  4
 furthest = 0
            ^
```

## Step by step

At each index, first check that we can stand on it (`i <= furthest`), then extend the edge with `i + jump`.

```text
i=0  jump=2   0 <= 0 ok   furthest = max(0, 0+2) = 2     reach: [0..2]
i=1  jump=3   1 <= 2 ok   furthest = max(2, 1+3) = 4     reach: [0..4]
i=2  jump=1   2 <= 4 ok   furthest = max(4, 2+1) = 4
i=3  jump=1   3 <= 4 ok   furthest = max(4, 3+1) = 4
i=4  jump=4   4 <= 4 ok   furthest = 8
loop ends -> True
```

Now a failing input, `[3, 2, 1, 0, 4]`:

```text
 index:     0  1  2  3  4
 value:     3  2  1  0  4

i=0  furthest = 3
i=1  furthest = max(3, 3) = 3
i=2  furthest = max(3, 3) = 3
i=3  furthest = max(3, 3) = 3      the 0 adds nothing
i=4  4 > 3 -> return False         index 4 is beyond the block

  [0 1 2 3] | 4        every path piles up on the 0 at index 3
```

## Why it works

Because reachable indices form a prefix block, an index `i` is reachable exactly when `i <= furthest` at the time we get to it. Each reachable index can only push the edge outward, so keeping the maximum of `i + jump` is all the state needed. If we ever reach an index past the edge, nothing earlier can land beyond the edge, so nothing later can be reached either.

## Where it goes wrong

- Checking `i > furthest` after updating `furthest` instead of before. The update would then let an unreachable index extend the reach.
- Treating a zero as fatal. In `[2, 0, 0]` the first jump passes over both zeros. Zeros only block when `furthest` stops at them.
- A single element `[0]` is already at the last index, so the answer is `True`; the loop accepts index 0 since `0 <= 0`.

## Cost

Time O(n): one pass. Space O(1): the single number `furthest`.
