## The idea

Detecting whether a cycle exists is the easy part: send a slow pointer (one step) and a fast pointer (two steps) from the head. If there is a cycle the fast one laps the slow one inside it and they meet. If there is none, the fast one falls off the end.

Finding where the cycle begins takes one more observation. Let `a` be the number of steps from the head to the cycle entry and `c` the cycle length. When they meet, slow has walked `a + k` for some `k` inside the cycle, and fast has walked twice that. Fast has gone round the cycle some whole number of extra times, so `a + k` is a multiple of `c`. That means starting at the meeting point and walking `a` more steps lands exactly on the entry. A new pointer from the head also needs `a` steps to reach the entry. So two pointers moving one step at a time, one from the head and one from the meeting point, collide at the entry.

A hash set of visited nodes also works but costs O(n) space.

## Set-up

- `slow` and `fast` both start at `head`.
- Phase 1 loop condition `fast and fast.next` protects the double step.
- After the meeting, `slow` is reset to `head`, and `fast` stays at the meeting point but now moves one step at a time.

```text
 3 ──▶ 2 ──▶ 0 ──▶ -4
       ▲            │
       └────────────┘

 a = 1 step from the head to the entry (node 2), cycle length c = 3
```

## Step by step

Phase 1, with positions given as node values:

```text
start     slow=3    fast=3
round 1   slow=2    fast=0      (3 -> 2 -> 0)
round 2   slow=0    fast=2      (0 -> -4 -> 2)
round 3   slow=-4   fast=-4     slow is fast: they meet at -4
```

Phase 2: `slow` goes back to the head, both move one step:

```text
start     slow=3    fast=-4     different
step 1    slow=2    fast=2      (fast: -4 -> 2)  same node: the entry
return the node with value 2
```

The meeting point `-4` is 2 steps into the cycle (k = 2) and `a + k = 3 = c`, matching the argument above.

## Why it works

At the meeting, slow has walked `a + k` and fast `2(a + k)`. Their difference, `a + k`, is a whole number of laps, so `a + k` is a multiple of `c`. Therefore `a` more steps from the meeting point (which is `k` into the cycle) brings you to the position `a + k` laps back, which is the entry. The pointer from the head reaches the entry in `a` steps too.

## Where it goes wrong

- Forgetting `fast.next` in the loop condition. When `fast` is the last node, `fast.next.next` would crash.
- Moving the pointers with different speeds in phase 2. Both now go one step at a time.
- Returning the meeting node instead of the node found in phase 2. The meeting point is generally somewhere inside the cycle, not the entry.
- A list without a cycle ends the loop and returns `None`; an empty list or one node does too.

## Cost

Time O(n): phase 1 takes at most about `a + c` rounds, phase 2 takes `a`. Space O(1): two pointers.
