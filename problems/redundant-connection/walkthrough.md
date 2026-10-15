## The idea

A tree on n nodes has n - 1 edges. We are given n edges, so exactly one edge is extra, and adding it closed a loop. Add the edges one at a time. While the graph is still a forest, each new edge joins two separate pieces. The first edge whose two ends are already in the same piece is the one that closes the cycle.

"Are these two nodes already connected?" is what union-find answers fast.

## Set-up

- `parent[x]` points toward the representative (root) of `x`'s group. Nodes are labelled from 1, so the array has `len(edges) + 1` slots and `parent[0]` is unused.
- Everyone starts as their own parent: `parent = list(range(n + 1))`.
- `find(x)` follows parents to the root, and shortens the path as it goes (path halving: `parent[x] = parent[parent[x]]`).

The invariant: two nodes share a root exactly when the edges processed so far connect them.

```text
edges = [1,2] [2,3] [3,4] [1,4] [1,5]

node    : 0  1  2  3  4  5
parent  : 0  1  2  3  4  5
```

## Step by step

For each edge, find both roots. If they match, return the edge. Otherwise `parent[root_a] = root_b`.

```text
edge [1,2]  roots 1, 2   different -> parent[1] = 2
            parent: 0 2 2 3 4 5
edge [2,3]  roots 2, 3   different -> parent[2] = 3
            parent: 0 2 3 3 4 5
edge [3,4]  roots 3, 4   different -> parent[3] = 4
            parent: 0 2 3 4 4 5       (chain 1 -> 2 -> 3 -> 4)
edge [1,4]  find(1): 1 -> 2 -> 3 -> 4; halving sets parent[1]=3
            and parent[3]=4
            roots 4, 4   SAME -> return [1, 4]
```

```text
the cycle:     1 ─── 2
               │     │        edge [1,4] closes it
               4 ─── 3        edge [1,5] never gets looked at
```

## Why it works

Every edge we merge joins two different groups, so the accepted edges always form a forest. The first edge to connect two nodes in one group must be on a cycle with the path that already joins them. Since exactly one cycle exists, the edges before the closing one form a tree-like forest, and the closing edge is the last cycle edge in input order. That is the one the task wants, because dropping any cycle edge leaves a tree and the answer must be the latest one.

## Where it goes wrong

- Comparing `a` and `b` directly instead of their roots. `find(1)` and `find(4)` match, but `1 != 4`.
- Setting `parent[a] = b` instead of `parent[root_a] = root_b`, which splits groups wrongly and breaks the invariant.
- Making `parent` of size `len(edges)`: node n would index out of range, since labels start at 1.

## Cost

Time O(n * alpha(n)), effectively linear: alpha is the inverse Ackermann function, tiny for any real input. Path halving does the compression. Space O(n) for `parent`.
