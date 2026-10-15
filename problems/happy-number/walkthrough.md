## The idea

Replace a number by the sum of the squares of its digits and repeat. Either you land on 1 (happy, and 1 maps to itself) or you never do. The values cannot grow without bound: even a 10-digit number maps to something below 1000, and from there values stay small. So the sequence lives in a finite set, which means it must either hit 1 or repeat and loop forever.

The question becomes: does this sequence end at 1, or enter a cycle? That is the same as detecting a cycle in a linked list, with `next_value` as the "next pointer".

## Set-up

- `next_value(x)` returns the sum of squares of the digits of `x`.
- `slow` starts at `n` and moves one step per round.
- `fast` starts one step ahead, at `next_value(n)`, and moves two steps per round.

Invariant: `fast` is always ahead of `slow` on the same sequence. If the sequence cycles, `fast` laps `slow` and they become equal. If it reaches 1, `fast` gets there first.

## Step by step

For `n = 19` the sequence is 19, 82, 68, 100, 1:

```text
start     slow = 19   fast = 82
round 1   slow = 82   fast = next(next(82)) = next(68) = 100
round 2   slow = 68   fast = next(next(100)) = next(1) = 1
fast == 1, the loop stops, return True.
```

For an unhappy number, `n = 2`, the sequence runs 2, 4, 16, 37, 58, 89, 145, 42, 20, 4, ...:

```text
start     slow = 2     fast = 4
round 1   slow = 4     fast = 37
round 2   slow = 16    fast = 89
round 3   slow = 37    fast = 42
round 4   slow = 58    fast = 4
round 5   slow = 89    fast = 37
round 6   slow = 145   fast = 89
round 7   slow = 42    fast = 42    slow == fast, stop
fast != 1, so return False.
```

```text
 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -+
 ^                                             |
 +---------------------------------------------+
```

## Why it works

Inside a cycle, `fast` closes the gap to `slow` by one each round, so they must meet. Because 1 maps to itself, a happy sequence reaches 1 and `fast` sits there (and the loop condition catches it). Stopping on `fast == 1` therefore means happy, and stopping on `slow == fast` with `fast != 1` means a cycle that excludes 1.

## Where it goes wrong

Starting both at `n` would make `slow != fast` false immediately, so the loop would not run. That is why `fast` starts one step ahead. The final answer is `fast == 1`, not `slow == fast`: the pointers can also coincide on 1 or on a cycle, and only the first is happy.

## Other approaches

`solution_set.py` stores every value seen in a set and stops when it hits 1 or a repeat. It is simpler, and the number of distinct values is small, but it needs extra memory that Floyd's method avoids.

## Cost

Each step costs O(log n) for the digits. The number of steps is bounded by a constant since values quickly fall below 1000 and the cycle is short. Space is O(1) for Floyd, or O(number of distinct values) for the set.
