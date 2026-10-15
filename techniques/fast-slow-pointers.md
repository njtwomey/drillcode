---
title: Fast and slow pointers
area: Linked lists
topics: [Linked list, Two pointers]
problems:
  - middle-of-the-linked-list
  - linked-list-cycle
  - remove-nth-node-from-end-of-list
  - reorder-list
  - find-the-duplicate-number
related: [dummy-head, in-place-reversal]
---

## Reach for it when

- You need the middle of a list.
- You need to detect a cycle, or find where it starts.
- You need the kth node from the end in one pass.
- An array holds values that are indices ("treat it as a linked list").

## Setup

- `slow = fast = head`. Invariant: `fast` has made exactly twice the steps of `slow`, so when `fast` falls off the end `slow` is halfway.
- Loop `while fast and fast.next:` then `slow = slow.next; fast = fast.next.next`. Both tests keep `fast.next.next` from touching `None`.
- For a fixed gap of n, advance a lead pointer n steps first, then move both one step at a time. Invariant: the gap never changes.

## Template

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def cycle_entry(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None


nodes = [ListNode(i) for i in range(6)]
for a, b in zip(nodes, nodes[1:]):
    a.next = b
nodes[-1].next = nodes[2]
assert cycle_entry(nodes[0]) is nodes[2]
nodes[-1].next = None
assert cycle_entry(nodes[0]) is None
```

## What it removes

A second pass or extra memory. Finding the middle would otherwise need the length first. Cycle detection would otherwise need a set of visited nodes. The kth from the end would otherwise need the length. Two walkers at different speeds, or at a fixed gap, answer each of these in one pass with O(1) space.

## Pitfalls

- Testing only `fast` and not `fast.next`. An even-length list raises `AttributeError` on `fast.next.next`.
- Picking the wrong middle. `while fast and fast.next` gives the second middle of an even list, which is what `middle-of-the-linked-list` wants. `while fast.next and fast.next.next` gives the first middle, which is the right cut in `reorder-list`.
- In the array version, testing `slow == fast` before moving. Both start at the same place, so the test is true at once. `find-the-duplicate-number` uses `while True` and tests after the first move.
- Comparing node values rather than nodes. Use `is`, since values repeat.
- Resetting both pointers in the second phase of Floyd. Reset one to the start; the other stays at the meeting point.

## Variants

- Middle: `middle-of-the-linked-list` returns `slow` after the loop.
- Cycle test: `linked-list-cycle` returns `True` when `slow is fast`. The gap inside the cycle shrinks by one per step, so `fast` must land on `slow`.
- Fixed gap: `remove-nth-node-from-end-of-list` starts both at a dummy node and advances `fast` n + 1 steps, so `slow` stops before the target. See `dummy-head`.
- Middle as a split: `reorder-list` cuts at the first middle with `slow.next = None`, then reverses the second half. See `in-place-reversal`.
- Cycle entry: `find-the-duplicate-number` treats `nums[i]` as the next pointer of index `i`. Phase one finds a meeting point. Phase two restarts `slow` at `nums[0]` and advances both one step; they meet at the duplicate.

## Worked example

Problem: `middle-of-the-linked-list`

The loop stops when `fast` runs off the end.

```python
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
```

The setup line and the loop condition are the template's. On an odd list `fast` stops on the last node. On an even list `fast` becomes `None` and `slow` is the second of the two middles, as the problem requires.
