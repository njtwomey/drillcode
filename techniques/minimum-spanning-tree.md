---
title: Minimum spanning tree
area: Graphs
topics: [Graph, Heap]
problems:
  - min-cost-to-connect-all-points
related: [union-find, weighted-shortest-paths, heap-patterns, graph-building-and-dfs]
---
## Reach for it when
- You must connect every node at the lowest total edge cost, and the connections need not be paths between particular pairs.
- The statement says "connect all", "cheapest network", "cables" or "roads", and the answer is a sum of edge weights.
- Edges are implied by coordinates (Manhattan distance) rather than listed.
- Do not use it for a cheapest path between two nodes. That is `weighted-shortest-paths`.

## Setup
- Two properties justify both algorithms. Cut property: the cheapest edge crossing any split of the nodes into two sides belongs to some minimum spanning tree. Cycle property: the dearest edge on any cycle belongs to no minimum spanning tree (when it is strictly dearest).
- A spanning tree has exactly `n - 1` edges. Stop when you have taken that many.
- Prim grows one tree. `visited` holds the nodes in it, and `heap` holds `(weight, node)` pairs for edges leaving it. `total` is the cost so far. Invariant: the tree built so far is part of a minimum spanning tree.
- Prim on a complete graph can use an array instead: `cheapest[i]` is the cost of the cheapest edge joining `i` to the tree, and each round takes the outside node with the smallest value.
- Kruskal sorts all edges, then takes each edge whose endpoints are in different components. It needs the `parent` and `find` from `union-find`. `taken` counts accepted edges.

## Template
```python
import heapq
from collections import defaultdict


def mst_cost(n, edges):
    graph = defaultdict(list)
    for a, b, w in edges:
        graph[a].append((b, w))
        graph[b].append((a, w))
    visited = set()
    heap = [(0, 0)]
    total = 0
    while heap and len(visited) < n:
        w, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        total += w
        for nxt, cost in graph[node]:
            if nxt not in visited:
                heapq.heappush(heap, (cost, nxt))
    return total if len(visited) == n else -1
```

## What it removes
- It removes any search over subsets of edges. The cut and cycle properties make the greedy choice safe.
- On a complete graph the array form of Prim removes both the heap and the edge list. There are about `n^2` edges, so building and sorting them costs more than scanning arrays.
- Kruskal removes the need to track a growing tree. The `union-find` structure answers "would this edge make a cycle" in nearly constant time.

## Pitfalls
- Adding an edge only when it is cheap, without the cycle test. Kruskal then builds a cycle and overcounts.
- Directed edges. Add both directions for Prim. A spanning tree is undirected.
- Forgetting the stale-entry skip in Prim with a heap. A node can be pushed by several tree nodes; only the first pop counts. Without `if node in visited: continue` its cost is added more than once.
- Not checking connectivity. If `len(visited) < n` the graph has no spanning tree. The template returns `-1`.
- Mixing up the keys. In Prim the heap key is the edge weight, not the distance from the start. Using `d + w` turns it into Dijkstra and gives a wrong total.
- Sorting `n(n-1)/2` edges for large `n`. Kruskal on a complete graph is O(n^2 log n), while the array form of Prim is O(n^2).
- A single point. The answer is 0: `cheapest[0] = 0` is added in the only round.

## Variants
- Prim on arrays: `min-cost-to-connect-all-points` keeps `cheapest` and `visited` as lists. Each of `n` rounds picks the unvisited `u` with the smallest `cheapest[u]` via `min(..., key=cheapest.__getitem__)`, adds it to `total`, then lowers `cheapest[v]` for the outside points using Manhattan distance. No edge list is built.
- Kruskal with union-find: `solution_kruskal.py` of the same problem builds every `(dist, i, j)` for `i < j`, sorts, then walks the edges. It merges when `find(i) != find(j)` (joined with `parent[root_i] = root_j`, no size list) and stops once `taken == n - 1`.
- Choose by density. Kruskal suits a given sparse edge list. Prim with a heap suits an adjacency list. The array form of Prim suits a complete graph.
- Related but different: `redundant-connection` on `union-find` is Kruskal's cycle test on its own.

## Worked example
Problem: `min-cost-to-connect-all-points`

Every pair of points is an edge with Manhattan weight. The solution grows the tree from point 0 and always attaches the cheapest outside point.

```python
class Solution:

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        cheapest = [float('inf')] * n
        cheapest[0] = 0
        visited = [False] * n
        total = 0
        for _ in range(n):
            u = min((i for i in range(n) if not visited[i]), key=cheapest.__getitem__)
            visited[u] = True
            total += cheapest[u]
            for v in range(n):
                if not visited[v]:
                    dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                    if dist < cheapest[v]:
                        cheapest[v] = dist
        return total
```

`visited` and `total` are the template's. `cheapest` replaces the heap: the `min` over the unvisited points is the heap pop, and the inner loop is the push, lowering a key in place instead of adding a stale entry. Each round adds one point, so after `n` rounds the tree spans everything.
