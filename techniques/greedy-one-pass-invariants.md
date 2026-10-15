---
title: One pass with a tracked quantity
area: Greedy
topics: [Greedy]
problems:
  - jump-game
  - best-time-to-buy-and-sell-stock
  - non-overlapping-intervals
  - container-with-most-water
  - majority-element
  - jump-game-ii
  - gas-station
  - candy
  - partition-labels
related: [interval-patterns, opposite-ends, dp-finding-the-state, prefix-and-suffix-passes]
---
## Reach for it when
- One number seems enough to decide each step: the minimum so far, the furthest reachable index, the end of the last kept interval.
- The problem asks for a value (a count, a profit, true or false), not a reconstruction.
- Sorting first would make the local choice safe (earliest end, smallest start).
- A local rule is easy to state, and an exchange argument for it comes to mind.

## Setup
- One variable, updated once per element: `furthest`, `lowest`, `last_end`. The loop never looks back.
- A `best` or `result` for the answer when it differs from the tracked value (`lowest` versus `best` profit in `best-time-to-buy-and-sell-stock`).
- Sort first if the rule depends on order: `non-overlapping-intervals` sorts by end.
- Layer boundaries, when the answer counts steps: `end` is the last index reachable with the current count, and `farthest` the last index reachable with one more. Invariant: when `i == end`, the layer is used up and the count goes up by one.
- A forced-end marker, when a cut is allowed only once something is satisfied: `end` is the farthest index the current part must reach, and `start` the first index of the part.
- Two quantities when the rule is one-directional: a restart point `start` and a running `tank`, plus a `total` over the whole input.
- Invariant: after element `i`, the tracked value is the optimum of its kind over elements `0..i`.

## Template
The reach version: track the furthest index reachable and fail when the current index passes it.

```python
def one_pass(nums):
    furthest = 0
    for i, num in enumerate(nums):
        if i > furthest:
            return False
        furthest = max(furthest, i + num)
    return True
```

## What it removes
- The DP table. A tracked number replaces `dp[i]` for every `i`, because the future depends only on that number.
- Pair enumeration. `best-time-to-buy-and-sell-stock` needs profit `price - lowest`, not every buy/sell pair.
- Backtracking over which intervals to keep. After sorting by end, one comparison with `last_end` decides each interval.

## Pitfalls
- A greedy that passes the examples and fails a crafted input. This is the technique to be most suspicious of. Before trusting one, state the exchange argument in one sentence, such as "any solution that skips the earliest-ending interval can be changed to one that takes it without getting worse". If no such sentence exists, it is probably DP.
- Sorting by the wrong key. Sorting `non-overlapping-intervals` by start fails on `[[1, 100], [2, 3], [4, 5]]`.
- Using `>` instead of `>=` for touching intervals. `[[1, 2], [2, 3]]` do not overlap, so `start >= last_end` keeps the second.
- Updating the tracked value in the wrong order. In the stock problem, update `lowest` first so a same-day sale gives 0, never a negative number.
- In `jump-game-ii`, looping to the last index. The loop must stop one before it, or the final index closes a layer and adds a jump that is not needed.
- In `gas-station`, resetting `tank` but not moving `start` to `i + 1`, or returning `start` without checking `total >= 0`. The first gives the wrong station; the second returns a station when the circle has a deficit.
- In `candy`, one pass only, or assigning instead of taking the max on the second pass. A peak between two slopes then loses one of them, for example ratings `[1, 2, 3, 1]` give the peak 2 candies instead of 3.
- In `partition-labels`, cutting on `i == last[c]` for the current letter alone rather than on the running maximum `end`. Parts split too early and a letter appears in two parts.
- In `jump-game`, checking `i > furthest` after the update instead of before. The failure on `[3, 2, 1, 0, 4]` is then missed.

## Variants
- Furthest reach: `jump-game` (`furthest = max(furthest, i + jump)`, return false when `i > furthest`).
- Minimum so far: `best-time-to-buy-and-sell-stock` (`lowest` and `best`).
- Sort then keep: `non-overlapping-intervals`, sorted by end, counting removals.
- A tracked pair, not one number: `majority-element` carries a `candidate` and a `count` (Boyer-Moore voting). Each value that differs from the candidate cancels one vote; at `count == 0` the next value becomes the candidate. The answer is correct only because a majority is guaranteed to exist; on input without one it returns some value anyway, so a verification pass would be needed.
- Shrink from both ends: `container-with-most-water` moves the shorter wall inward. It is two pointers rather than one pass, but the justification is the same kind: any container that keeps the shorter wall is narrower and no taller.
- Layers of reach, `jump-game-ii`: `farthest = max(farthest, i + nums[i])` each step; when `i == end`, add a jump and set `end = farthest`. A greedy form of breadth-first search, with no queue.
- Restart on failure, `gas-station`: `tank` collects `gas[i] - cost[i]` and `total` collects the same over the circle. When `tank < 0`, no start in `[start, i]` can work, so set `start = i + 1` and `tank = 0`. Return `start` if `total >= 0`, else -1.
- Two passes, `candy`: `candies = [1] * n`; left to right, a child rated above the left neighbour gets `candies[i - 1] + 1`; right to left, the same for the right neighbour with `max`. The answer is `sum(candies)`. See `prefix-and-suffix-passes`.
- Cut when the forced end is reached, `partition-labels`: `last` maps each letter to its final index. `end = max(end, last[c])`; at `i == end` record `end - start + 1` and set `start = i + 1`.

## Worked example
Problem: `jump-game`

Each index either lies within reach or the walk stops. One variable carries all the information from the earlier jumps.

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        # furthest = farthest index reachable using the positions seen so far (greedy).
        furthest = 0
        for i, jump in enumerate(nums):
            # A gap: no earlier jump reaches i, and nothing later can jump back over it.
            if i > furthest:
                return False
            furthest = max(furthest, i + jump)
        return True
```

`furthest` is the tracked quantity and starts at 0, the index we stand on. The check `i > furthest` is the failure test, made before the update. `max(furthest, i + jump)` is the only state change, so the loop never looks back.
