## The idea

The minimum depth is the number of nodes on the shortest path from the root down to a leaf. A leaf is a node with no children at all.

A recursive "1 + min(left, right)" looks natural but has a trap, covered below. Breadth-first search avoids it. Visit the tree one level at a time, from the top; the first leaf you meet is on the shallowest level that has one, so you can return immediately without looking at the rest of the tree.

## Set-up

- `level` is the list of nodes on the current depth. It starts as `[root]`.
- `depth` is the depth of `level`, counting the root as 1.
- `nxt` collects the children of this level, becoming the next `level`.

Invariant: every node on a shallower level than `level` has already been checked and was not a leaf.

For the tree `[3, 9, 20, null, null, 15, 7]`:

```text
        3          depth 1
       / \
      9   20       depth 2
         /  \
        15   7     depth 3

level = [3]   depth = 1
```

## Step by step

```text
Round 1   level = [3]       depth = 1
          3 has children, so it is not a leaf.
          nxt = [9, 20]

Round 2   level = [9, 20]   depth = 2
          9 has no left and no right child: a leaf.
          return 2
```

Node 20 and everything under it are never looked at. A depth-first search would have gone through all five nodes.

## Why it works

Levels are processed in increasing depth, and inside a level every node is checked before moving on. So the first leaf found has the smallest possible depth. Nodes with exactly one child are not leaves, so the code only follows the child that exists (`if node.left`, `if node.right` each guard themselves).

## Where it goes wrong

The recursive shortcut `1 + min(depth(left), depth(right))` treats a missing child as depth 0. On a node with one child that wrongly counts the empty side as a path.

```text
  1
   \
    2         true answer: 2  (root to leaf 2)

min(0, 1) + 1 = 1   wrong, because node 1 is not a leaf
```

The BFS never has this problem: a node is only accepted when both children are `None`. An empty tree returns 0 up front, and a single node returns 1 in the first round.

## Cost

Time O(n) in the worst case (for example when the only leaf is at the bottom), but often much less since it stops at the first leaf. Space O(n): the widest level of a balanced tree holds about half the nodes.
