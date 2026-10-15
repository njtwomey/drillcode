---
title: Use the BST ordering
area: Trees
topics: [Tree]
problems:
  - validate-binary-search-tree
  - kth-smallest-element-in-a-bst
  - lowest-common-ancestor-of-a-binary-search-tree
related: [tree-recursion-return-and-best, binary-search-shapes]
---
## Reach for it when

- "BST" or "binary search tree" is in the title.
- The question is about order: is it valid, the kth smallest, a common ancestor, a search.
- A general-tree solution works but ignores the ordering, which costs O(n) where the ordering allows O(h).

## Setup

- Validate: `low` and `high` per node, starting at `None, None` (unbounded). Each node must satisfy `low < val < high` strictly. The left child gets `(low, node.val)` and the right child `(node.val, high)`. The solution carries them on an explicit `stack` of `(node, low, high)` tuples. The notes call these `lo` and `hi`; the solution uses `low` and `high`.
- Kth smallest: `stack = []`, `node = root`, and `k` counted down. The stack holds the ancestors whose left subtree is still being visited.
- LCA: `node = root`, and the walk moves down with no extra memory.
- Invariant: bounds come from all ancestors. In-order visits values in ascending order.

## Template

```python
def in_order_kth(root, k):
    stack = []
    node = root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    return -1
```

This is the kth smallest solution. Validate and LCA are in Variants and the worked example.

## What it removes

It removes searching both subtrees. In a BST, comparing with the node's value picks one side, so LCA walks one path in O(h) and uses O(1) space. In-order traversal removes sorting: the values arrive sorted, and the walk can stop at the kth.

## Pitfalls

- Comparing a node only with its parent. A node deep in the right subtree can be smaller than the grandparent and still pass the local check. The bounds must come from all ancestors.
- Duplicates. LeetCode's BST definition is strict, so equal values are invalid: reject with `<=` and `>=`.
- Integer limits as bounds. A node can hold `-2**31` or `2**31 - 1`, so a sentinel of that size is wrong; use `None` or infinity.
- Kth smallest: decrementing `k` after the pop but checking before it gives an off-by-one. Count when you pop, not when you push.
- Using the BST walk in LCA when the tree is not a BST. Use `tree-recursion-return-and-best`.

## Variants

- `validate-binary-search-tree`: pass `(low, high)` down. The solution pushes `(node.left, low, node.val)` and `(node.right, node.val, high)` on a `stack`. An in-order traversal that checks strictly increasing values also works.
- `kth-smallest-element-in-a-bst`: iterative in-order with a `stack`. Push the left spine, pop and count, then go right. Stop at `k == 0`. Time is O(h + k).
- `lowest-common-ancestor-of-a-binary-search-tree`: if both values are smaller than `node.val`, go left. If both are larger, go right. Otherwise `node` is the answer, including when one target equals `node`.

## Worked example

Problem: `validate-binary-search-tree`

The bounds travel with each node on an explicit stack.

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # Each stack entry carries the open interval (low, high) its node must fall in.
        # The bounds come from ALL ancestors, not just the parent, which is why a node
        # deep in the right subtree can still be invalid against the grandparent.
        # Iterative to avoid recursion-depth limits on skewed trees.
        stack = [(root, None, None)]
        while stack:
            node, low, high = stack.pop()
            if node is None:
                continue
            # <= and >= (not < and >) so duplicates are rejected. None means unbounded,
            # which avoids picking a sentinel that node values could equal.
            if (low is not None and node.val <= low) or (high is not None and node.val >= high):
                return False
            # Left subtree must stay below this node; right subtree must stay above it.
            # The other bound is inherited unchanged.
            stack.append((node.left, low, node.val))
            stack.append((node.right, node.val, high))
        return True
```

`low` and `high` start as `None`, meaning unbounded. The `<=` and `>=` reject duplicates. Pushing `(node.left, low, node.val)` tightens the upper bound for the left child, and `(node.right, node.val, high)` tightens the lower bound for the right child. The other bound is inherited unchanged.
