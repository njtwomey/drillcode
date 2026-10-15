## The idea

A node is good if no node on the path from the root to it has a bigger value. You could, for each node, walk up and check all its ancestors, but that repeats work. Instead walk down once and carry the answer to "what is the biggest value so far on this path?" in a single number, `best`.

At each node, compare its value with `best`. If it is at least as big, the node is good. Then pass `max(best, node.val)` down to the children.

## Set-up

- `dfs(node, best)` returns how many good nodes are in the subtree at `node`. `best` is the largest value among the node's ancestors.
- The first call is `dfs(root, root.val)`. The root has no ancestors, so it is always good, and starting `best` at its own value makes `root.val >= best` true. Starting at `0` would be wrong for negative values.
- A `None` node contributes 0 and ends the recursion.

## Step by step

Tree `[3,1,4,3,null,1,5]`:

```text
            3
           / \
          1   4
         /   / \
        3   1   5
```

Each node with the `best` it receives and the verdict:

```text
node  best-in  good?   best-out
 3       3     3>=3 yes    3
 1       3     1>=3 no     3
 3       3     3>=3 yes    3     (under the 1; equal counts as good)
 4       3     4>=3 yes    4
 1       4     1>=4 no     4
 5       4     5>=4 yes    5
```

Four good nodes: the root 3, the lower 3, the 4, and the 5. The call tree adds up as `count + left + right` at each level:

```text
dfs(3,3) = 1 + dfs(1,3) + dfs(4,3)
dfs(1,3) = 0 + dfs(3,3) = 0 + 1 = 1
dfs(4,3) = 1 + dfs(1,4) + dfs(5,4) = 1 + 0 + 1 = 2
total = 1 + 1 + 2 = 4
```

## Why it works

`best` is exactly the maximum over all ancestors, because each level takes the max of its parent's `best` and its own value. So `node.val >= best` is exactly the definition of good. Each node is visited once with its own path's maximum; different branches never interfere because `best` is passed by value.

## Where it goes wrong

Comparing against the parent instead of the maximum ancestor. In `[3,1,null,null,2]` the 2 is bigger than its parent 1, but not bigger than 3:

```text
    3
   /
  1          2 vs parent 1: looks good (wrong)
   \         2 vs best 3:   not good  (right)
    2
```

Also use `>=`, not `>`: a node equal to the maximum is still good.

## Cost

Time O(n): each node once. Space O(h) for the recursion, where h is the tree height (n for a chain).
