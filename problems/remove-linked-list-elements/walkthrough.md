## The idea

Deleting a node from a singly linked list means making the node before it skip over it. So you do not stand on the node you want to delete; you stand on its predecessor and look at `prev.next`.

That creates a problem for the head, which has no predecessor. A dummy node placed in front of the list gives every real node, including the head, a predecessor. Then there is a single rule for all nodes.

## Set-up

- `dummy` is a throwaway node whose `next` is `head`. Its value is never read.
- `prev` is the last node we have decided to keep. It starts at `dummy`.

Invariant: everything from `dummy` to `prev` is already clean (no node with value `val`), and `prev.next` is the next node to judge.

Take `[6, 1, 6, 6, 2]` with `val = 6`:

```text
dummy ──▶ 6 ──▶ 1 ──▶ 6 ──▶ 6 ──▶ 2 ──▶ None
 prev
```

## Step by step

Look at `prev.next` each round. If it matches, bypass it and leave `prev` where it is. Otherwise advance `prev`.

```text
Round 1  prev.next = 6, match: prev.next = prev.next.next
         dummy ──▶ 1 ──▶ 6 ──▶ 6 ──▶ 2
          prev

Round 2  prev.next = 1, no match: prev moves forward
         dummy ──▶ 1 ──▶ 6 ──▶ 6 ──▶ 2
                   prev

Round 3  prev.next = 6, match: bypass
         dummy ──▶ 1 ──▶ 6 ──▶ 2
                   prev

Round 4  prev.next = 6 again, match: bypass
         dummy ──▶ 1 ──▶ 2
                   prev

Round 5  prev.next = 2, no match: prev moves forward
         dummy ──▶ 1 ──▶ 2 ──▶ None
                         prev
```

`prev.next` is `None`, so the loop ends. Return `dummy.next`, which is node 1. The leading 6 was removed without any special case.

## Why it works

Each round either deletes the node after `prev` or confirms it is clean and steps over it. The part up to `prev` is never revisited, and `prev.next` always names the first undecided node, so every node gets judged exactly once.

## Where it goes wrong

Advancing `prev` after a deletion. Two matching nodes in a row show why not:

```text
dummy ──▶ 1 ──▶ 6 ──▶ 6 ──▶ 2          val = 6
          prev

Wrong: bypass the first 6, then move prev onto the second 6.
       dummy ──▶ 1 ──▶ 6 ──▶ 2          the second 6 now survives
```

Returning `head` instead of `dummy.next` is the other classic mistake: the old head may have been deleted. An empty list gives `dummy.next` equal to `None`, and a list where everything matches ends up empty too.

## Cost

Time O(n): each node is looked at once. Space O(1): one dummy node and one pointer.
