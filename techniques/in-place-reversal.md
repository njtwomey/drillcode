---
title: In-place reversal
area: Linked lists
topics: [Linked list]
problems:
  - reverse-linked-list
  - reorder-list
  - palindrome-linked-list
  - reverse-linked-list-ii
  - reverse-nodes-in-k-group
related: [fast-slow-pointers, dummy-head]
---

## Reach for it when

- You must reverse a list or part of one.
- O(1) extra space is required.
- The task is "reorder" or "palindrome" on a list, which means walking from both ends.

## Setup

- `prev = None`: the head of the already-reversed part. At the start it is empty.
- `curr = head`: the head of the untouched rest.
- `nxt`: assigned inside the loop. It holds `curr.next` before the link is overwritten.
- Return `prev`.

## Template

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev, curr = curr, nxt
    return prev


head = None
for v in [3, 2, 1]:
    head = ListNode(v, head)
head = reverse(head)
out = []
while head:
    out.append(head.val)
    head = head.next
assert out == [3, 2, 1]
assert reverse(None) is None
```

## What it removes

The extra memory of copying values into an array or building a new list. Each node is re-pointed once, so the reversal is O(n) time and O(1) space. It also gives access to a list from the tail end without back pointers.

## Pitfalls

- Overwriting `curr.next` before saving it. The rest of the list is lost and the loop ends after one node.
- Returning `curr`. It is `None` when the loop ends; the new head is `prev`.
- In `reorder-list`, not setting `slow.next = None` before the weave. The first half still points into the reversed half and the result contains a cycle.
- In `reverse-nodes-in-k-group`, reversing before checking that `k` nodes remain. The short last group is reversed too: `[1, 2, 3, 4, 5]` with `k = 3` must give `[3, 2, 1, 4, 5]`, not `[3, 2, 1, 5, 4]`.
- Reversing a sub-range without reconnecting its ends. The node before the range must be pointed at the new range head, and the old range head must be pointed at what followed.

## Variants

- Reverse a whole list: `reverse-linked-list`.
- Reverse the second half, then walk both halves together: `reorder-list`. It finds the cut with `fast-slow-pointers`, reverses the half after it, and interleaves. `palindrome-linked-list` is the same shape with a comparison at the end.
- Reverse the second half, then compare: `palindrome-linked-list` runs the template loop on `slow` instead of `head`, so `prev` ends as the head of the reversed half. It then compares `left = head` with `right = prev`. The list is left half-reversed, which the problem allows.
- Pull to the front: `reverse-linked-list-ii` does not flip links one at a time. `before` is the node ahead of position `left` and `curr = before.next` is the segment's first node, which never moves. Each of `right - left` rounds takes `nxt = curr.next`, unlinks it, and inserts it at `before.next`. `curr` ends as the segment tail, already linked to the rest. A dummy covers `left == 1`.
- Reverse in groups: `reverse-nodes-in-k-group` first walks `kth` forward `k` nodes from `group_prev` and returns if the list ends first, so a short remainder stays in order. It then runs the template loop with `prev` started at `group_next`, the first node of the following group, instead of `None`. The old group head is then already linked onward. `group_prev.next` is set to the new head, and `group_prev` moves to the old head, the group's tail.
- Recursive: `reverse-linked-list` also has `solution_recursive.py`. Reverse `head.next`, then set `head.next.next = head` and `head.next = None`. It uses O(n) stack space.

## Worked example

Problem: `reverse-linked-list`

The iterative version, one pass.

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
```

`prev` and `curr` are the template's two pointers, and `nxt` is the saved reference. The two assignments at the end advance both. When `curr` is `None`, `prev` is the old tail and so the new head.
