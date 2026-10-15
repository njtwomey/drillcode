## The idea

Reversing a list means every node's `next` has to point at the node that used to come before it. A singly linked list only knows its successors, so there is no way to "look back". The trick is to build the answer as you go: keep the part you have already reversed in one hand and the part you have not touched in the other, and move one node at a time from the second to the first.

Each move is the same three actions: remember what comes next, turn the current node around, step forward.

## Set-up

Three references are enough:

- `prev` is the head of the reversed part. It starts as `None`, because nothing has been reversed yet, and that `None` is what the old head will end up pointing at.
- `curr` is the head of the untouched part. It starts at `head`.
- `nxt` is a temporary hold on `curr.next`, taken before we overwrite it.

```text
 prev    curr
  │       │
 None     1 ──▶ 2 ──▶ 3 ──▶ None
 (reversed)   (untouched)
```

## Step by step

Each round runs `nxt = curr.next`, then `curr.next = prev`, then `prev = curr`, then `curr = nxt`. Here is `1 → 2 → 3`, with the arrows that changed drawn in the new direction:

```text
Round 1   nxt = 2.  Turn node 1 around, then step forward.

  None ◀── 1        2 ──▶ 3 ──▶ None
          prev     curr

Round 2   nxt = 3.  Turn node 2 around, then step forward.

  None ◀── 1 ◀── 2        3 ──▶ None
                 prev    curr

Round 3   nxt = None.  Turn node 3 around, then step forward.

  None ◀── 1 ◀── 2 ◀── 3        None
                       prev     curr
```

`curr` has run off the end, so the loop stops. `prev` is the old tail, which is now the head of `3 → 2 → 1`.

## Why it works

At the top of every round the list is split into two valid pieces: `prev` heads a correctly reversed list, `curr` heads an untouched list, and together they hold every node exactly once. One round moves one node across the seam and keeps both pieces valid. When the untouched piece is empty, everything has been reversed, and `prev` is its head.

## Where it goes wrong

The order of the first two lines matters. If you write `curr.next = prev` first, the pointer to node 2 is gone and the rest of the list is lost. That is the whole reason `nxt` exists.

```text
Wrong order, round 1:   curr.next = prev   (1 now points at None)
                        nxt = curr.next    (nxt is None, not 2)

  None ◀── 1        2 ──▶ 3        ← nothing points at 2 any more
```

Returning `curr` instead of `prev` is the other classic slip: at the end `curr` is `None`.

## The recursive version

The recursive form (the `reverseListRecursive` variant) lets the call stack hold what `nxt` held. Reverse everything after `head`, then hook `head` onto the end of the result:

```text
reverse(1 → 2 → 3)
  reverse(2 → 3)
    reverse(3)          returns 3
  2.next.next = 2       3 ──▶ 2
  2.next = None         3 ──▶ 2 ──▶ None
1.next.next = 1         3 ──▶ 2 ──▶ 1
1.next = None           3 ──▶ 2 ──▶ 1 ──▶ None
```

It reads nicely but uses one stack frame per node, so a list of a few thousand nodes can hit Python's recursion limit. The loop does not.

## Cost

Time O(n): each node is visited once. Space O(1): three references, whatever the length. The recursive version is O(n) space for the call stack.
