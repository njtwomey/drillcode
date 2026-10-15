## The idea

We want to know whether some path from the root down to a leaf adds up to `targetSum`. Instead of summing the whole path at every leaf, carry a number down the tree: how much is still needed. Each node subtracts its own value from it. At a leaf, the path works exactly when nothing is left over, that is, `remaining == 0`.

## Set-up

- `remaining` is `targetSum - root.val`: the amount the rest of the path, below this node, must still supply.
- The base case is `root is None`, returning `False`.
- A leaf is a node with no left and no right child. Only a leaf can finish a path.

Invariant: when a call is made on a node, the `targetSum` it receives is the original target minus all the values above it.

```text
          5
        /   \
       4     8
      /     / \
    11    13   4
   /  \
  7    2          target = 22
```

## Step by step

The code tries the left subtree first and only goes right if that returns `False`.

```text
hasPathSum(5, 22)     remaining = 17
  hasPathSum(4, 17)   remaining = 13
    hasPathSum(11, 13)  remaining = 2
      hasPathSum(7, 2)    remaining = -5, leaf   ──▶ False
      hasPathSum(2, 2)    remaining =  0, leaf   ──▶ True
    11 returns True
  4 returns True
5 returns True
```

The path found is 5, 4, 11, 2 which sums to 22. The `or` stops as soon as one side is `True`, so node 8 and its children are never visited.

## Why it works

Every root-to-leaf path is explored by some chain of calls, and along that chain `remaining` equals the target minus the sum so far. At the leaf, `remaining == 0` means the sum is exactly the target. If any path succeeds, `or` carries that `True` back up the stack.

## Where it goes wrong

A missing child must return `False`, not be treated as a leaf. If the base case compared the remainder to 0 on `None`, a node with one child could "end" a path on its empty side:

```text
   1
  /          target = 1
 2

Wrong: node 1 has remaining 0, its right child is None -> treat as end, True
Right: 1 is not a leaf (it has a left child), so go down to 2:
       remaining = -1, leaf  ──▶ False
```

An empty tree is `False` even when the target is 0, because there is no path at all. Negative values are fine, since we only test equality at a leaf and never prune early.

## Cost

Time O(n): in the worst case every node is visited once. Space O(h) for the call stack, where h is the tree height (O(n) for a chain, O(log n) when balanced).
