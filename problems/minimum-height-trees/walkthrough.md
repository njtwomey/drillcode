## The idea

Rooting a tree at a node gives a height equal to the distance to the farthest node. The best roots are the centres of the tree, the middle of its longest path. A path has one middle node if its length is even in edges, or two if odd, so the answer has one or two nodes.

We find the centre by peeling: remove all the leaves, then remove the new leaves, and so on, like peeling an onion. What is left at the end is the centre.

## Set-up

- `n <= 2` is answered right away: every node is a valid root.
- `adj[i]` is the set of neighbours of node `i`.
- `leaves` is the current layer of nodes with exactly one neighbour.
- `remaining` is how many nodes are still in the tree. We stop once it is 2 or less.

## Step by step

`n = 6`, edges `3-0, 3-1, 3-2, 3-4, 5-4`.

```text
   0   1   2          adj: 0:{3}  1:{3}  2:{3}
    \  |  /                3:{0,1,2,4}
      3                    4:{3,5}   5:{4}
      |
      4
      |
      5

leaves = [0, 1, 2, 5]   remaining = 6
```

Round 1: `remaining = 6 - 4 = 2`. Each leaf is cut from its neighbour.

```text
leaf 0: nxt=3, adj[3] = {1,2,4}    3 still has 3 edges
leaf 1: nxt=3, adj[3] = {2,4}
leaf 2: nxt=3, adj[3] = {4}        one edge left -> 3 is a new leaf
leaf 5: nxt=4, adj[4] = {3}        one edge left -> 4 is a new leaf

leaves = [3, 4]
```

```text
 3 ── 4        remaining is 2, loop stops
```

The answer is `[3, 4]`. Check: rooting at 3 gives height 2 (3 to 4 to 5), and no other root does better.

With a path `0 - 1 - 2`, the leaves are `[0, 2]`, `remaining` drops to 1, and removing them leaves node 1 as the single new leaf, so the answer is `[1]`.

## Why it works

Peeling a layer of leaves shortens every longest path by one on each end, so the middle of those paths stays put. Repeating until one or two nodes remain lands on the middle of the longest path, which is where the farthest distance is smallest.

## Where it goes wrong

- Without the `n <= 2` early return, a single node has no leaves (zero neighbours), and the loop logic breaks.
- Stopping at `remaining > 2` rather than `> 0` matters: peeling past the centre would remove it.
- A node must only be added to `next_leaves` when it drops to exactly one edge; zero edges means it is the last node and is already in `next_leaves`.

## Cost

Time O(n): each node and edge is processed once. Space O(n) for the adjacency sets and leaf lists.
