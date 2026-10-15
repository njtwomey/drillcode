---
title: Dummy head
area: Linked lists
topics: [Linked list]
problems:
  - merge-two-sorted-lists
  - add-two-numbers
  - remove-nth-node-from-end-of-list
  - merge-k-sorted-lists
  - lru-cache
related: [fast-slow-pointers, in-place-reversal]
---

## Reach for it when

- The head might change or be removed.
- A list is being built node by node.
- Two or more lists are being merged into one.
- A doubly linked list needs insert and remove at both ends.

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
- Forgetting the leftover after a merge loop ends. `[1, 3]` merged with `[2, 4, 5]` loses `4, 5` unless you attach `list1 or list2` afterwards.
- In `add-two-numbers`, looping only while a list has nodes. `5 + 5` drops the final carry digit; the loop must also run while `carry` is non-zero.
- In `merge-k-sorted-lists`, pushing `node.next` before reading it, or comparing `ListNode` objects on equal values. The heap tuples carry an index so nodes are never compared.

## Variants

- Building: `tail` appends to the result. `merge-two-sorted-lists` relinks existing nodes and ends with `tail.next = list1 or list2`. `add-two-numbers` creates new nodes. `merge-k-sorted-lists` pops the smallest head from a heap and relinks it.
- Editing: `prev` stays one node behind the work. In `remove-nth-node-from-end-of-list` the dummy is also the start of the gap, so `slow` stops before the node to remove, even when that node is the head. See `fast-slow-pointers`.
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
