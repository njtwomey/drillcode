---
title: Divide and conquer
area: Divide and conquer
topics: [Tree, Linked list, Binary search]
problems:
  - sort-list
  - convert-sorted-array-to-binary-search-tree
  - median-of-two-sorted-arrays
related: [fast-slow-pointers, dummy-head, binary-search-shapes, bst-invariant]
---
## Reach for it when
- The problem on `n` items can be built from the same problem on two halves plus a cheap combine step.
- You must sort a linked list in O(n log n) with little extra memory.
- You must build a balanced tree from sorted data.
- An O(log) bound is asked for on a problem that involves two sorted sequences.

## Setup
- A base case that stops the split: an empty range or a single item is already solved.
- A split point `mid`. For arrays and ranges it is `(lo + hi) // 2`. For a linked list it comes from `slow` and `fast`.
- Two recursive calls on strictly smaller parts. Invariant: each call returns a finished answer for its half.
- A combine step whose cost is at most linear (merge, link a node), so the total is O(n log n).
- When the data is an array, pass index bounds `lo, hi` instead of slices, to avoid copying.

## Template
```python
def merge_sort(items):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

## What it removes
It removes the quadratic work of handling items one against all others. Halving gives about log2(n) levels, each doing linear work. On a linked list it removes random access: merge sort needs only sequential access and relinking. For the BST it removes rebalancing: choosing the middle makes the shape balanced by construction.

## Pitfalls
- A split that does not shrink. In `sort-list`, starting `fast` at `head` makes a two-node list split into 2 and 0, so the recursion never ends. The solution starts `fast = head.next`.
- Forgetting to cut the list: without `slow.next = None` the first half still runs into the second.
- Not attaching the leftover in a merge. When one side runs out, `tail.next = a or b` appends the other whole.
- Taking from the right side on ties, which makes the sort unstable. The merge uses `a.val <= b.val`.
- Slicing arrays at every level costs O(n) per call. Pass `lo, hi`, as `convert-sorted-array-to-binary-search-tree` does.
- Off by one at the split: `build(lo, mid)` instead of `build(lo, mid - 1)` repeats `nums[mid]` and never terminates.
- In the median search, binary search on the longer array: `j = half - i` can leave `b`. Search the shorter one.

## Variants
- Merge sort on a linked list (`sort-list`): `slow, fast = head, head.next` finds the end of the first half, `second = slow.next` and `slow.next = None` cut it. The recursive results go to `merge`, which uses a `dummy` and `tail` and appends the leftover with `a or b`. Time is O(n log n), and the recursion depth is O(log n).
- Balanced BST from a sorted array (`convert-sorted-array-to-binary-search-tree`): `build(lo, hi)` returns `None` when `lo > hi`, makes the root from `nums[mid]`, and recurses on `lo..mid - 1` and `mid + 1..hi`. The sorted order gives the BST property, and the two sides differ in size by at most one.
- Partition search (`median-of-two-sorted-arrays`): the halving is on the answer, not the data. Binary search on the cut `i` in the shorter array, with `j = half - i` in the other, until every left element is `<=` every right element. There is no merge step. The solution is iterative, not recursive, and uses O(log min(m, n)) time. See `binary-search-shapes` for the loop.
- Pairwise merge of `k` lists would also fit this page, but the catalogue's `merge-k-sorted-lists` uses a heap, so it is not listed here.

## Worked example
Problem: `sort-list`

The list is cut at the end of its first half, each half is sorted by the same method, and the sorted halves are merged.

```python
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None
        return self.merge(self.sortList(head), self.sortList(second))

    def merge(self, a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next
```

The first `if` is the base case. The `slow` and `fast` loop is the split, and `slow.next = None` cuts it. The two recursive calls are the template's `left` and `right`, and `merge` is the combine step. It uses `dummy` as in `dummy-head`, with `tail` as the write end of the output. The merged list is `dummy.next`.
