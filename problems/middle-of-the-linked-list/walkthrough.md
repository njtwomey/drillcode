## The idea

A linked list does not know its own length, so finding the middle seems to need two passes: count, then walk half the count. Two pointers do it in one. Let one pointer move a step at a time and the other two steps at a time. When the fast one reaches the end, the slow one has covered half the distance, so it is standing at the middle.

## Set-up

- `slow` moves one node per round.
- `fast` moves two nodes per round.
- Both start at `head`.

Invariant: `fast` is always exactly twice as far from `head` as `slow`.

```text
 slow
 fast
  │
  1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ 5 ──▶ None
```

## Step by step

The loop runs while `fast` and `fast.next` both exist, because we are about to jump two nodes. First the odd list `1..5`:

```text
Start     slow=1  fast=1
          1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ 5
          S,F

Round 1   slow=2  fast=3
          1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ 5
                S     F

Round 2   slow=3  fast=5
          1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ 5
                      S           F
```

`fast.next` is `None`, so the loop stops. `slow` is on node 3, the exact middle. Returning it gives `3 → 4 → 5`.

Now an even list `1..4`:

```text
Start     1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ None
          S,F
Round 1   1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ None
                S     F
Round 2   1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ None
                      S              F (None)
```

`fast` is now `None`, the loop stops, and `slow` is on 3. Two nodes tie for the middle (2 and 3), and this loop lands on the second one, which is what the problem asks for.

## Why it works

After `k` rounds `slow` has moved `k` nodes and `fast` has moved `2k`. `fast` falls off the end when `2k` reaches the length, so `k` is about half the length, and that is where `slow` is. For odd lengths `fast` stops on the last node; for even lengths it steps past it. Either way the same loop gives the right node.

## Where it goes wrong

Checking only `fast` is not enough. On an odd list `fast` lands on the last node, and `fast.next.next` would then read through `None`.

```text
1 ──▶ 2 ──▶ 3        fast on 3, fast.next is None
                     fast.next.next  ──▶ error
```

That is why the condition is `fast and fast.next`. A single node returns itself: the loop never starts.

## Cost

Time O(n): `fast` makes about n/2 jumps. Space O(1): two pointers.
