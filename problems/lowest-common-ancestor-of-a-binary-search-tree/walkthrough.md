## The idea

In a general tree you would have to search both subtrees to find where two nodes meet. A binary search tree already tells you where each value lives: smaller goes left, larger goes right. So at any node you can look at `p.val` and `q.val` and decide where to go without searching.

The lowest common ancestor is the first node, walking down from the root, where `p` and `q` stop going the same way.

## Set-up

- `node` starts at `root` and only ever moves down.
- No other state is needed.

Invariant: both `p` and `q` are somewhere in the subtree rooted at `node`.

## Step by step

```text
          6
        /   \
       2     8
      / \
     0   4
        / \
       3   5
```

Find the LCA of `p = 3` and `q = 5`.

```text
node 6:  3 < 6 and 5 < 6   both smaller  -> node = node.left   (2)
node 2:  3 > 2 and 5 > 2   both larger   -> node = node.right  (4)
node 4:  3 < 4 but 5 > 4   they split    -> return 4
```

Now `p = 2`, `q = 4`:

```text
node 6:  2 < 6 and 4 < 6   both smaller  -> node = node.left   (2)
node 2:  p.val == 2        neither "both smaller" nor "both larger"
                                         -> return 2
```

## Why it works

While both values lie on the same side of `node`, every common ancestor of the two must be on that side too, so moving there loses nothing. The first node where they are on different sides, or where one of them equals `node`, is an ancestor of both, and no deeper node can be, because the walk would then separate them. That node is the lowest one.

## Where it goes wrong

Use strict comparisons for the two "same side" tests. If `p.val == node.val`, the node is itself an ancestor of `p` (a node counts as its own ancestor), so it must be returned, not skipped. Using `<=` in the tests would walk past it and return a node that is too low.

Do not use the general tree solution here. It works but ignores the ordering and costs O(n).

## Cost

Time O(h), where h is the height: one step down per round. Space O(1), since the walk is a loop with no recursion. A balanced tree gives O(log n); a chain-shaped tree gives O(n).
