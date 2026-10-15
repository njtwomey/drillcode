## The idea

The houses form a binary tree, and robbing a node forbids robbing its parent and children. A plain "rob this node or not" recursion revisits the same subtrees many times, because the grandchildren get explored both from the node and from its children.

The fix is to have each node report two answers at once: the best haul from its subtree if the node itself is robbed, and the best if it is not. A parent can then decide using only its children's pairs, with no repeated work.

## Set-up

`dfs(node)` returns `(take, skip)`:

- `take` is the best total for this subtree when `node` is robbed. Both children must then be skipped.
- `skip` is the best total when `node` is not robbed. Each child is free, so we use whichever of its two numbers is larger.
- An empty node returns `(0, 0)`.

The recursion is post-order: both children are solved before the parent combines them.

```text
tree:        3
           /   \
          4     5
         / \     \
        1   3     1
```

## Step by step

Results come back bottom-up. For a node, `take = val + left_skip + right_skip` and `skip = max(left_take, left_skip) + max(right_take, right_skip)`.

```text
dfs(1, left of 4)    (1, 0)      leaf: take=1, skip=0
dfs(3, right of 4)   (3, 0)
dfs(4)               take = 4 + 0 + 0 = 4
                     skip = max(1,0) + max(3,0) = 4         -> (4, 4)

dfs(1, under 5)      (1, 0)
dfs(5)               left is None -> (0, 0)
                     take = 5 + 0 + 0 = 5
                     skip = 0 + max(1,0) = 1                -> (5, 1)

dfs(3, root)         take = 3 + 4 + 1 = 8
                     skip = max(4,4) + max(5,1) = 9         -> (8, 9)
```

`max(dfs(root))` is `max(8, 9) = 9`. The best plan skips the root and robs 4's children (1 and 3) plus 5, giving 1 + 3 + 5 = 9.

## Why it works

For every subtree, the pair holds the true optimum under each of the two possible states of its root. A parent's options depend on its children only through those two states, so combining the pairs is exact. Each node is computed once.

## Where it goes wrong

Skipping a node does not force robbing its children. Writing `skip = left_take + right_take` is a common mistake: it forgets that a child may also be skipped, which is better when the child is small and its own child is big.

```text
   1          dfs(9) = (9, 0)
   │          dfs(2) = (2, 9)      take 2, or skip 2 and keep the 9
   2
   │          for the root's skip:
   9            wrong:  left_take             = 2
                right:  max(left_take, left_skip) = max(2, 9) = 9
```

Always take the `max` of each child's pair:

```text
wrong:  skip = left_take + right_take
right:  skip = max(left_take, left_skip) + max(right_take, right_skip)
```

## Cost

Time O(n): each node is visited once and does constant work. Space O(h) for the recursion stack, where h is the tree height (up to n for a chain).
