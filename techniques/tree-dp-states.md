---
title: Return a tuple of states
area: Trees
topics: [Tree, Dynamic programming]
problems:
  - house-robber-iii
  - binary-tree-cameras
  - binary-tree-maximum-path-sum
  - diameter-of-binary-tree
related: [tree-recursion-return-and-best, dp-finding-the-state, tree-top-down-state]
---
## Reach for it when

- A choice at a node (rob it, put a camera on it) changes what the neighbouring nodes are allowed to do.
- The natural recursion "best for this subtree" is not enough, because the parent needs to know how the node was left: taken or skipped, covered or not.
- A plain recursive "take or skip" would revisit the same subtrees again and again, and you would otherwise reach for a memo keyed on the node.

## Setup

- An inner `def dfs(node)` that returns a small fixed tuple, one entry per state the parent cares about. The solutions name them `(take, skip)` for house-robber-iii, and three constants `NEEDS, COVERED, CAMERA` for binary-tree-cameras.
- Base case for `None`: the tuple (or state) that is neutral for the parent. `(0, 0)` for a haul. `COVERED` for cameras, because a missing child needs nothing and must not force a camera above it.
- Post-order: call `dfs` on both children first, unpack their tuples, then build this node's tuple from them.
- `best` or `cameras`: a counter under `nonlocal` when the answer is accumulated on the way rather than read from the root's tuple.
- Invariant: each tuple entry is the optimum for the node's subtree under that state, so the parent never looks below its children.

## Template

```python
def best_haul(root):
    def dfs(node):
        if node is None:
            return 0, 0
        left_take, left_skip = dfs(node.left)
        right_take, right_skip = dfs(node.right)
        take = node.val + left_skip + right_skip
        skip = max(left_take, left_skip) + max(right_take, right_skip)
        return take, skip

    return max(dfs(root))
```

Run on a tree `3(2(-, 3), 3(-, 1))` it gives 7. The worked example is this template for house-robber-iii.

## What it removes

It removes the memo dictionary and the repeated work. "Rob the node or not" written as two recursive calls that each recurse into grandchildren is exponential, and a dictionary keyed on nodes fixes that at the cost of memory and bookkeeping. Returning both outcomes from one visit makes it one O(n) pass with O(h) stack.

## Pitfalls

- Assuming that skipping a node forces its children to be taken. It does not. `skip` is `max(left_take, left_skip) + max(right_take, right_skip)`. Using only `left_take + right_take` fails on a chain where the best answer skips two levels.
- Returning only `take` or only `skip` as the answer. The answer is `max(dfs(root))`.
- A wrong base case. Returning `(0, 0)` is right for a haul. For cameras, returning `NEEDS` for `None` puts a camera on every leaf's parent for no reason, and returning `CAMERA` hides leaves that need cover.
- Cameras: placing a camera on a leaf. Cover a leaf from its parent, because that camera also watches the grandparent. Check order in the solution matters: any child `NEEDS` comes first, then any child `CAMERA`, otherwise this node `NEEDS`.
- Cameras: forgetting the root. It has no parent, so if `dfs(root) == NEEDS` add one more camera. A single-node tree answers 1, not 0.
- Forgetting `nonlocal` on the counter when it is reassigned or incremented inside `dfs`.
- Deep trees hit the recursion limit, as in any recursive tree walk.

## Variants

- `house-robber-iii`: returns `(take, skip)`. Taking the node forces both children skipped (`node.val + left_skip + right_skip`). Skipping frees each child to take its better outcome.
- `binary-tree-cameras`: returns one of three states rather than a tuple of values, and counts `cameras` as a side effect. `NEEDS` if both children are `COVERED`, `CAMERA` (and `cameras += 1`) if any child `NEEDS`, `COVERED` if any child has a `CAMERA`. This is a greedy choice (cameras as high as possible) written in the same shape.
- `binary-tree-maximum-path-sum` and `diameter-of-binary-tree`: the relatives where `dfs` returns one number (the downward leg) and records a different one (the path that bends here) in `best`. Described in `tree-recursion-return-and-best`.

## Worked example

Problem: `house-robber-iii`

`dfs` returns the best haul for a subtree in both states, and the parent combines them.

```python
class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        # dfs(node) returns (take, skip): the best haul from node's subtree if the node
        # itself is robbed, and if it is not. Returning both lets a parent decide without
        # revisiting children, which a plain "rob or skip" recursion would do repeatedly.
        def dfs(node):
            if node is None:
                return 0, 0
            left_take, left_skip = dfs(node.left)
            right_take, right_skip = dfs(node.right)

            # Robbing this node forces both children to be skipped.
            take = node.val + left_skip + right_skip
            # Skipping it frees each child to be either robbed or skipped, whichever is better.
            skip = max(left_take, left_skip) + max(right_take, right_skip)
            return take, skip

        return max(dfs(root))
```

The `None` case `(0, 0)` is the neutral base. The two unpacked pairs are the children's states, and `take` and `skip` are built only from them. `max(dfs(root))` picks the better state at the root.
