## The idea

This is the ordinary list reversal done on one block of `k` nodes at a time, with two extra jobs: make sure the block really has `k` nodes before touching it, and stitch the reversed block back into the list on both sides.

The neat trick is where the reversal starts. Normally `prev` starts as `None`. Here it starts as the first node of the next group, so when the old first node of the block is turned around, it already points on to the rest of the list. Only the front link needs fixing afterwards.

## Set-up

- `dummy` points at `head`. Reversing the first block changes the head, and the dummy gives that block a predecessor to relink.
- `group_prev` is the node just before the current block. It begins at `dummy`.
- `kth` walks `k` steps from `group_prev` to the last node of the block. If it falls off the list, the leftover is shorter than `k` and stays as it is.
- `group_next` is the node after `kth`, the start of the next block.
- `prev`, `curr`, `nxt` are the usual reversal references, with `prev` starting at `group_next`.

```text
k = 2
dummy ──▶ 1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ 5
  ^group_prev   ^kth  ^group_next
```

## Step by step

```text
Block 1: reverse 1,2 with prev = 3
   curr=1: 1.next = 3          prev=1  curr=2
   curr=2: 2.next = 1          prev=2  curr=3 (== group_next, stop)

   tail = group_prev.next = 1   (still the old first node)
   dummy.next = prev = 2
   group_prev = tail = 1

   dummy ──▶ 2 ──▶ 1 ──▶ 3 ──▶ 4 ──▶ 5
                   ^group_prev

Block 2: kth = 4, group_next = 5, prev = 5
   3.next = 5, then 4.next = 3, so prev = 4
   tail = 1.next = 3
   1.next = 4
   group_prev = 3

   dummy ──▶ 2 ──▶ 1 ──▶ 4 ──▶ 3 ──▶ 5
                               ^group_prev

Block 3: kth walks 3 -> 5 -> None. Fewer than 2 nodes left, so return.
```

The result is `2 → 1 → 4 → 3 → 5`.

## Why it works

Before each block, everything up to `group_prev` is final and correctly linked. Reversing one block with `prev = group_next` leaves the block internally reversed and its tail pointing at the unprocessed rest. Setting `group_prev.next = prev` joins the front. The tail of the new block is the old first node, so it becomes the next `group_prev`.

## Where it goes wrong

- Reading `tail = group_prev.next` after `group_prev.next = prev` gives the new head, not the old one. The order matters.
- Reversing before counting leaves a short remainder reversed, which is wrong. That is why `kth` is checked first.
- `k = 1` works naturally: each block reverses to itself.

## Cost

Time O(n): the `kth` walk and the reversal each touch every node once. Space O(1): a handful of references.
