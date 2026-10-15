---
title: Carry state down the recursion
area: Trees
topics: [Tree]
problems:
  - path-sum
  - path-sum-ii
  - count-good-nodes-in-binary-tree
  - path-sum-iii
  - minimum-depth-of-binary-tree
  - validate-binary-search-tree
related: [tree-recursion-return-and-best, tree-dp-states, bst-invariant, prefix-sums-and-hashing, backtracking-template]
---
## Reach for it when

- The condition at a node depends on the path from the root: a remaining target, the maximum so far, the allowed value range.
- The statement says "root to leaf path", "good node", "path that starts anywhere going downward".
- The answer is built from decisions made on the way down, not from the children's answers.

## Setup

- An inner `def dfs(node, state)` with the state as an extra parameter. Immutable state (an int, a bound) needs no cleanup: each call gets its own copy. The solutions use `remaining`, `best` (the maximum on the path) and `prefix`.
- `path = []` and `result = []` when the paths themselves are wanted. Push on entry, pop on exit, copy with `path[:]` when recording.
- `seen = {0: 1}` for the prefix-sum count: how many nodes on the current root path have each prefix sum, including the empty prefix. Undo the increment on exit.
- Leaf test: `node.left is None and node.right is None`. A missing child is not a leaf.
- Invariant: when `dfs(node, state)` starts, `state` describes exactly the path from the root to the parent of `node`, and any shared mutable structure (`path`, `seen`) holds exactly that path.

## Template

```python
def root_to_leaf_paths(root, target):
    result = []
    path = []

    def dfs(node, remaining):
        if node is None:
            return
        path.append(node.val)
        remaining -= node.val
        if node.left is None and node.right is None and remaining == 0:
            result.append(path[:])
        else:
            dfs(node.left, remaining)
            dfs(node.right, remaining)
        path.pop()

    dfs(root, target)
    return result
```

Run on the tree `5(4(11(7, 2)), 8(13, 4(5, 1)))` with target 22 it returns `[[5, 4, 11, 2], [5, 8, 4, 5]]`. This is the path-sum-ii solution.

## What it removes

It removes the re-summing of paths and the second traversal. Passing `remaining` down turns "does this path sum to the target" into a comparison with zero at the leaf. For the prefix map, one running sum plus a dictionary replaces summing from every ancestor, taking path-sum-iii from O(n^2) in the worst case to O(n).

## Pitfalls

- Treating a missing child as a leaf. For `[1, 2]` and target 1, the missing right child would match. Test that both children are `None`, or return `False` for `None`.
- Recording a match at a non-leaf in path-sum-ii: check the leaf condition together with `remaining == 0`.
- Appending `path` itself instead of `path[:]`. Every recorded path then becomes the same list, which ends up empty.
- Missing the `path.pop()` on one exit branch. Later siblings then start from the wrong prefix.
- Prefix sum: not seeding `seen = {0: 1}`. Paths that start at the root are never counted.
- Prefix sum: not decrementing `seen[prefix]` on exit. A sibling subtree then counts paths through nodes that are not its ancestors. Look the count up before inserting the current prefix, or a target of 0 counts the node against itself.
- Seeding `best` with `0` or `float("-inf")` instead of `root.val` in count-good-nodes. The root is always good, and the tree may be all negative.
- Comparing with the parent instead of the path maximum. A node is good only if no ancestor is larger, so pass `max(best, node.val)` down.
- Bounds as sentinels such as `2**31`. Use `None`, as the validate solution does.

## Variants

- `path-sum`: returns a bool. `remaining = targetSum - root.val` is passed down; at a leaf the answer is `remaining == 0`, otherwise `or` of the two children. `None` returns `False`.
- `path-sum-ii`: `path` and `result` shared across calls, push on entry, pop on exit, copy at a matching leaf. O(n^2) in the worst case because of the copies.
- `count-good-nodes-in-binary-tree`: `dfs(node, best)` returns a count. A node adds 1 if `node.val >= best`, then passes `max(best, node.val)` to both children and sums the results.
- `path-sum-iii`: paths may start and end anywhere going downward. `dfs(node, prefix)` looks up `seen.get(prefix - targetSum, 0)`, increments `seen[prefix]`, recurses, then decrements it. The dictionary is backtracked state like `path`. See `prefix-sums-and-hashing`.
- `minimum-depth-of-binary-tree`: the catalogue solution is a level-by-level BFS (`tree-bfs-by-level`), which stops at the first leaf. A top-down DFS version would carry `depth` and track a minimum at leaves, with the same leaf-versus-one-child rule.
- `validate-binary-search-tree`: the state is the open interval `(low, high)`. The solution carries it on an explicit `stack` of `(node, low, high)`, not through recursion, but the idea is the same. See `bst-invariant`.

## Worked example

Problem: `path-sum-iii`

The prefix-sum dictionary is state shared down the recursion, and it is undone on the way out.

```python
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # seen[s] is how many nodes on the current root-to-node path have prefix sum s,
        # counting the empty prefix (sum 0). A downward path ending here sums to the
        # target exactly when it starts just below an ancestor whose prefix is
        # (current prefix - target).
        seen = {0: 1}

        def dfs(node, prefix):
            if node is None:
                return 0
            prefix += node.val
            count = seen.get(prefix - targetSum, 0)

            seen[prefix] = seen.get(prefix, 0) + 1
            count += dfs(node.left, prefix) + dfs(node.right, prefix)
            # Leaving this node: remove it so the sibling subtree only sees its own ancestors.
            seen[prefix] -= 1
            return count

        return dfs(root, 0)
```

`prefix` is the immutable state passed down. `seen` starts as `{0: 1}`, the empty prefix, and is the mutable state that is pushed before the recursive calls and popped (`seen[prefix] -= 1`) after them, like `path` in the template. `count` is read before inserting the current prefix.
