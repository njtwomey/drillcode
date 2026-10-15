## The idea

A graph is a tree when it is connected and has no cycles. Checking both properties takes some work, but there is a shortcut: a tree on `n` nodes has exactly `n - 1` edges.

Given exactly `n - 1` edges, "no cycle" and "connected" imply each other. So check the edge count first, then just look for a cycle. With union-find, a cycle shows itself when an edge joins two nodes that are already in the same group.

## Set-up

- `len(edges) != n - 1` returns `False` immediately. Fewer edges cannot connect everything, and more must contain a cycle.
- `parent` is a union-find forest. Each node starts as its own root: `parent[i] = i`.
- `find(x)` follows parents to the root of `x`'s group, shortening the path as it goes (path halving).

Invariant: two nodes share a root exactly when the edges processed so far connect them.

```text
n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]       4 edges = n - 1, continue

parent = [0, 1, 2, 3, 4]       five groups of one
```

## Step by step

For each edge, find both roots. If they are equal, the edge closes a cycle. Otherwise attach one root under the other with `parent[ra] = rb`.

```text
edge (0,1)   roots 0 and 1, different. parent[0] = 1
             parent = [1, 1, 2, 3, 4]
edge (0,2)   roots 1 and 2, different. parent[1] = 2
             parent = [1, 2, 2, 3, 4]
edge (0,3)   roots 2 and 3, different. parent[2] = 3
             parent = [2, 2, 3, 3, 4]
edge (1,4)   roots 3 and 4, different. parent[3] = 4
             parent = [2, 3, 3, 4, 4]

No edge closed a cycle: return True.
```

Path halving has been at work: during the edge `(0,3)`, node 0 was re-pointed straight at 2 (skipping 1) while we searched.

Now a graph with a cycle, `n = 4`, `edges = [[0,1],[1,2],[2,0]]`. The edge count is 3 = `n - 1`, so it passes the first check.

```text
edge (0,1)   roots 0, 1. parent = [1, 1, 2, 3]
edge (1,2)   roots 1, 2. parent = [1, 2, 2, 3]
edge (2,0)   find(2) = 2.  find(0) = 2   (0 -> 1 -> 2)
             same root: cycle, return False.
```

Node 3 is left alone and disconnected, which is also why this is not a tree. The cycle check caught it because the count was right.

## Why it works

If there are `n - 1` edges and no edge ever joined two nodes already in the same group, then every edge merged two different groups. Starting from `n` groups, `n - 1` merges leave exactly one group, so the graph is connected. Connected with `n - 1` edges means it is a tree.

## Where it goes wrong

Skipping the edge count. Without it, `n = 4` with `[[0,1],[2,3]]` has no cycle but is two separate pieces, and would wrongly pass.

Comparing `parent[a]` to `parent[b]` instead of roots from `find` misses cycles through longer paths.

## Cost

Time O(n + E * alpha(n)), effectively linear, because path halving keeps `find` almost constant. Space O(n) for `parent`.
