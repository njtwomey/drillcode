---
title: In-place reversal
area: Linked lists
topics: [Linked list]
problems:
  - reverse-linked-list
  - reorder-list
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
- Reversing a sub-range without reconnecting its ends. The node before the range must be pointed at the new range head, and the old range head must be pointed at what followed.

## Variants

- Reverse a whole list: `reverse-linked-list`.
- Reverse the second half, then walk both halves together: `reorder-list`. It finds the cut with `fast-slow-pointers`, reverses the half after it, and interleaves. The same shape solves palindrome checks on a list.
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
