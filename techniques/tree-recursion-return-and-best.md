---
title: Return one thing, record another
area: Trees
topics: [Tree]
problems:
  - maximum-depth-of-binary-tree
  - same-tree
  - invert-binary-tree
  - subtree-of-another-tree
  - diameter-of-binary-tree
  - balanced-binary-tree
  - binary-tree-maximum-path-sum
  - lowest-common-ancestor-of-a-binary-tree
related: [tree-bfs-by-level, bst-invariant]
---
## Reach for it when

- The answer at a node is built from the answers of both children: height, balance, diameter, best path sum, lowest common ancestor.
- Two trees are walked in step (same tree, subtree of another tree).
- The quantity you want at a node is not the quantity a parent can use. A path that bends at a node is not extendable, but a downward leg is.

## Setup

- An inner `def dfs(node)` (the solutions name it `height` or `gain`) that returns a value the parent can extend.
- `best`: the running answer, declared in the outer function and updated with `nonlocal best`. A one-element list also works. For max path sum start at `float("-inf")` so all-negative trees work. For diameter `0` is enough.
- Base case `if node is None: return 0`. Use `None` for LCA and `-1` as a poison value for balance.
- Invariant: `dfs(node)` returns what a parent can extend; `best` holds the best through-the-node combination seen in any subtree visited so far.

## Template

```python
def best_through_node(root):
    best = 0

    def dfs(node):
        nonlocal best
        if node is None:
            return 0
        left = dfs(node.left)
        right = dfs(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    dfs(root)
    return best
```

This is the diameter solution, measured in edges. Swap in `max(0, ...)` clamps and `node.val` for max path sum.

## What it removes

It removes the second pass. Computing the height at every node by a separate call is O(n^2) on a skewed tree. Returning the height and recording the combination in the same visit makes it one O(n) pass. For balance, the `-1` value removes a separate "is balanced" walk.

## Pitfalls

- Returning the combination instead of the leg. If `dfs` returns `left + right`, the parent adds two legs of a path that already forks. Diameter and max path sum come out too large.
- Recording the leg instead of the combination. The answer is then only paths that start at a node and go down.
- Forgetting the clamp in max path sum: without `max(0, gain(child))` a negative subtree drags the sum down.
- Starting `best` at `0` in max path sum gives 0 instead of the largest single node on an all-negative tree.
- Forgetting `nonlocal best`: the assignment creates a local and the outer `best` stays at its start value (or raises `UnboundLocalError`).
- Diameter counts edges, not nodes. A single node has diameter 0.
- Recursion depth. Python's default limit is 1000 frames. A skewed tree of that depth raises `RecursionError`; raise it with `sys.setrecursionlimit` or write an iterative version. Pyodide honours the same limit.
- Subtree of another tree: the match must include every descendant, so use full equality (`same-tree`), not "values match as far as the smaller tree goes".

## Variants

- `maximum-depth-of-binary-tree`: only a return value, `1 + max(left, right)`. There is no `best`.
- `same-tree`: two nodes at once. Both `None` is true, exactly one `None` or unequal values is false, otherwise both pairs of children must match.
- `invert-binary-tree`: return the node after swapping `root.left, root.right = invert(root.right), invert(root.left)`.
- `subtree-of-another-tree`: for each node of the main tree, run the same-tree check against the subtree. O(m * n). The solution uses a helper `_same` for it.
- `diameter-of-binary-tree`: return the height; record `left + right`.
- `balanced-binary-tree`: return the height, or `-1` once any subtree is unbalanced. The `-1` passes up without exploring the right side.
- `binary-tree-maximum-path-sum`: return `node.val + max(left, right)` with both clamped at 0; record `node.val + left + right`.
- `lowest-common-ancestor-of-a-binary-tree`: return the node if it is `p` or `q`. If both children return something, the node is the answer; otherwise return whichever child returned something, with `left or right`.

## Worked example

Problem: `binary-tree-maximum-path-sum`

The two quantities are kept apart: `gain` returns one downward leg and `best` records the path that bends at a node.

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        # Two different quantities are in play:
        #  - best: the best path that bends at some node (uses both children).
        #  - gain() return value: the best path that goes only DOWN from a node, since
        #    a parent can extend just one branch.
        best = float("-inf")  # -inf (not 0) so all-negative trees are handled

        def gain(node):
            nonlocal best
            if node is None:
                return 0
            # A negative branch only hurts, so treat it as "don't take it" (0).
            left = max(0, gain(node.left))
            right = max(0, gain(node.right))
            # Candidate answer: this node is the top of the path, joining both sides.
            best = max(best, node.val + left + right)
            # Report upward only one side; a path can't fork when it continues up.
            return node.val + max(left, right)

        gain(root)
        return best
```

`best` is the template's `best`, set to `float("-inf")` and updated through `nonlocal`. `gain` is `dfs`. `left` and `right` are the clamped child legs. `best = max(best, node.val + left + right)` is the through-the-node record, and `return node.val + max(left, right)` is the extendable return.
