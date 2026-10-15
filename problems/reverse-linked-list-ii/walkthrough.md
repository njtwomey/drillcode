## The idea

Reversing a whole list is a standard loop. Reversing only the middle means the reversed part must also be reconnected to the nodes on either side. A tidy way to avoid that bookkeeping is to never flip links at all. Instead, take the first node of the segment (it will end up as the segment's tail) and repeatedly pull the node right after it to the front of the segment. Each pull moves one node into its reversed position, and the first node's own link to the rest of the list stays valid the whole time.

## Set-up

- `dummy` sits in front of `head`, so a segment starting at position 1 still has a node before it.
- `before` is the node just before position `left`. It walks `left - 1` steps from `dummy` and never moves afterwards. `before.next` is always the current front of the segment.
- `curr` is the node at position `left`. It does not move either: as nodes are pulled in front of it, it drifts toward the segment's end.
- `nxt` is the node right after `curr`, the next one to pull.

```text
list 1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5,  left = 2, right = 4

 dummy ─▶ 1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5 ─▶ None
         before curr
```

## Step by step

There are `right - left` pulls (here 2). Each runs: `nxt = curr.next`, `curr.next = nxt.next`, `nxt.next = before.next`, `before.next = nxt`.

```text
pull 1   nxt = 3.
         curr (2) now points past 3, to 4.
         3 points at the old segment front, 2.
         before (1) points at 3.

   dummy ─▶ 1 ─▶ 3 ─▶ 2 ─▶ 4 ─▶ 5 ─▶ None
           before     curr

pull 2   nxt = 4.
         curr (2) now points past 4, to 5.
         4 points at the old segment front, 3.
         before (1) points at 4.

   dummy ─▶ 1 ─▶ 4 ─▶ 3 ─▶ 2 ─▶ 5 ─▶ None
           before           curr
```

Return `dummy.next`: `1 → 4 → 3 → 2 → 5`.

## Why it works

After `k` pulls, the first `k + 1` nodes of the segment are already in reversed order, starting at `before.next` and ending at `curr`, and `curr.next` points to the untouched rest of the list. Each pull keeps that true for one more node. After `right - left` pulls the whole segment is reversed and `curr`, now its tail, already leads into the node after the segment.

## Where it goes wrong

- Writing `nxt.next = curr` instead of `nxt.next = before.next`. Pull 1 looks fine, but in pull 2 the node 4 points at 2 while `before` points at 4, and node 3 is lost.

```text
wrong after pull 2:   1 ─▶ 4 ─▶ 2 ─▶ 5        (3 dropped)
right after pull 2:   1 ─▶ 4 ─▶ 3 ─▶ 2 ─▶ 5
```

- Dropping the dummy. With `left == 1` the head changes and there is nothing to be `before`.
- Moving `curr` forward each round. It must stay on the original first node.

## Cost

Time O(n): one walk to `before` and at most `right - left` constant-time pulls. Space O(1).
