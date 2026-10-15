---
title: Dummy head
area: Linked lists
topics: [Linked list]
problems:
  - merge-two-sorted-lists
  - add-two-numbers
  - remove-nth-node-from-end-of-list
  - merge-k-sorted-lists
  - remove-linked-list-elements
  - swap-nodes-in-pairs
  - remove-duplicates-from-sorted-list-ii
  - reverse-linked-list-ii
  - reverse-nodes-in-k-group
  - odd-even-linked-list
  - lru-cache
related: [fast-slow-pointers, in-place-reversal]
---

## Reach for it when

- The head might change or be removed.
- A list is being built node by node.
- Two or more lists are being merged into one.
- A doubly linked list needs insert and remove at both ends.
- A run of nodes at the front (a duplicated head, a matching head, the first pair or group) may be removed or rewired.

## Setup

- `dummy = ListNode(0, head)`: a placeholder node whose `.next` is the real head. It is never part of the answer.
- `prev = dummy` when editing a list. Invariant: `prev.next` is the next node to examine, and everything up to `prev` is final.
- `tail = dummy` when building a list. Invariant: `tail` is the last node of the result so far, so `tail.next = ...` appends.
- Return `dummy.next`, never `head`.

## Template

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_all(head, target):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == target:
            prev.next = prev.next.next
        else:
            prev = prev.next
    return dummy.next


def build(values):
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


assert to_list(remove_all(build([1, 2, 1, 3, 1]), 1)) == [2, 3]
assert to_list(remove_all(build([1, 1]), 1)) == []
```

## What it removes

The special case for the first node. Without a dummy, the head has no predecessor, so removing or inserting at the front needs its own branch and its own return value. With a dummy, every real node is some node's `.next`. Removal is always `prev.next = prev.next.next` and insertion is always `prev.next = ListNode(v, prev.next)`.

## Pitfalls

- Returning `head`. If the old head was removed, the caller gets a node that is no longer in the list.
- Starting `prev` at `head` instead of `dummy`. The head can then never be removed.
- Advancing `prev` after a deletion. In `remove-linked-list-elements` and `remove-duplicates-from-sorted-list-ii` the node that moves up may also need to go, so `[1, 1, 1]` with target 1 leaves nodes behind. Advance `prev` only when the next node is kept.
- Rewiring a pair in the wrong order. In `swap-nodes-in-pairs`, setting `second.next = first` before `first.next = second.next` loses the rest of the list.
- Forgetting to move `prev` to the old first node after a swap or a group reversal. The next round then starts from the wrong predecessor and relinks nodes already placed.
- Forgetting the leftover after a merge loop ends. `[1, 3]` merged with `[2, 4, 5]` loses `4, 5` unless you attach `list1 or list2` afterwards.
- In `add-two-numbers`, looping only while a list has nodes. `5 + 5` drops the final carry digit; the loop must also run while `carry` is non-zero.
- In `merge-k-sorted-lists`, pushing `node.next` before reading it, or comparing `ListNode` objects on equal values. The heap tuples carry an index so nodes are never compared.

## Variants

- Building: `tail` appends to the result. `merge-two-sorted-lists` relinks existing nodes and ends with `tail.next = list1 or list2`. `add-two-numbers` creates new nodes. `merge-k-sorted-lists` pops the smallest head from a heap and relinks it.
- Editing: `prev` stays one node behind the work. In `remove-nth-node-from-end-of-list` the dummy is also the start of the gap, so `slow` stops before the node to remove, even when that node is the head. See `fast-slow-pointers`.
- Deleting by value: `remove-linked-list-elements` keeps `prev` one node behind and tests `prev.next.val == val`. A match is `prev.next = prev.next.next` with no advance, so a matching head or a run of matches needs no special case.
- Deleting whole runs: `remove-duplicates-from-sorted-list-ii` walks `curr` to the last node of a run of equal values and sets `prev.next = curr.next`. `prev` stays put because another run may follow, and a duplicated head is dropped like any other run.
- Rewiring in place: `swap-nodes-in-pairs` loops `while prev.next and prev.next.next`, names `first` and `second`, rewires `first.next`, `second.next`, `prev.next` in that order, then sets `prev = first`, which is now the tail of the pair.
- Sub-range reversal: `reverse-linked-list-ii` walks `before` to the node ahead of position `left`. The dummy covers `left == 1`. See `in-place-reversal`.
- Group reversal: `reverse-nodes-in-k-group` keeps `group_prev` as the node before each group. The dummy gives the first group a predecessor to relink. See `in-place-reversal`.
- No dummy needed: `odd-even-linked-list` never changes the head, so it returns `head` after an early exit for zero or one node. It builds two chains in place with `odd` and `even`, saves `even_head`, and ends with `odd.next = even_head`. The loop tests `even and even.next`.
- Two sentinels: `lru-cache` keeps a dummy head and a dummy tail in a doubly linked list. `_unlink` and `_push_front` never test for `None`, and eviction is `self.tail.prev`.

## Worked example

Problem: `merge-two-sorted-lists`

Two sorted lists are merged by repeatedly taking the smaller front node.

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = tail = ListNode()
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next
```

`dummy = tail = ListNode()` is the build setup. `tail` is the only variable that moves in the result, and the first attach is the same code as every other. `tail.next = list1 or list2` is the leftover step. `return dummy.next` skips the placeholder.
