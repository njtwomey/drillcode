---
title: Weighted shortest paths
area: Graphs
topics: [Graph, Heap]
problems:
  - network-delay-time
  - cheapest-flights-within-k-stops
  - swim-in-rising-water
related: [bfs-shortest-paths, heap-patterns, graph-building-and-dfs, minimum-spanning-tree]
---
## Reach for it when
- Edges have different costs (time, price, distance) and you want the cheapest path.
- The question is how long until a signal reaches every node, or the cheapest route from one source.
- A cap on the number of edges or stops is part of the question. That points to Bellman-Ford, not Dijkstra.
- The cost of a path is its worst edge or cell (the highest water level, the widest gap) rather than the sum.
- Edge weights may be zero or positive, and the graph is directed or undirected. Negative weights rule out Dijkstra.

## Setup
- `graph`: for each node a list of `(neighbour, weight)` pairs, built from the edge list. A directed edge is stored once.
- `dist = {}`: finalised distances. A node is added when it is popped, not when it is pushed. Invariant: every entry in `dist` is the true shortest distance.
- `heap = [(0, source)]`: pairs of `(distance so far, node)`. The smallest distance is popped first because tuples compare by their first item.
- The stale-entry skip: `if node in dist: continue`. A node can sit in the heap several times with different distances. The first pop is the smallest, so every later pop is stale.
- For Bellman-Ford with a hop limit: `cost = [INF] * n` with `cost[src] = 0`, and one round per allowed edge. After round `i`, `cost[v]` is the cheapest price to `v` using at most `i` edges.

## Template
```python
import heapq
from collections import defaultdict


def shortest_distances(n, edges, source):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = {}
    heap = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = d
        for nxt, w in graph[node]:
            if nxt not in dist:
                heapq.heappush(heap, (d + w, nxt))
    return dist
```

## What it removes
- The heap removes the scan for the closest unfinished node. Plain Dijkstra on arrays is O(V^2); the heap makes it O(E log V).
- The stale-entry skip removes `decrease-key`. Python's `heapq` cannot lower a priority, so you push a second entry and ignore the old one.
- Checking `len(dist) == n` removes a separate reachability pass.
- When all weights are equal, none of this is needed. `bfs-shortest-paths` finds the same answer with a plain queue and no heap.

## Pitfalls
- Negative weights. Dijkstra finalises a node on its first pop, which is only safe when no later path can be cheaper. With a negative edge the answer is wrong, with no error. Use Bellman-Ford.
- Forgetting the stale-entry skip. The answer stays right but each stale pop re-expands its node and the work can blow up. If you also record `dist` on push instead of on pop, a later cheaper path is lost.
- Returning the maximum of `dist` without checking `len(dist) == n`. A node that was never reached makes the answer `-1`, not the largest reached distance.
- Nodes labelled from 1. Index `n + 1` entries, or use a dict as the solution does.
- Bellman-Ford relaxed in place. One round can then chain several edges, and the hop limit is ignored. Relax from a snapshot of the previous round.
- Off by one on stops. `k` stops means `k + 1` flights, so run `k + 1` rounds.
- In `swim-in-rising-water`, pushing `best + grid[nr][nc]`. The cost of a path is the highest cell on it, so the pushed cost is `max(best, grid[nr][nc])`. A sum answers a different question.
- Relaxing from an unreached node. `cost[u] + price` with `cost[u] = INF` stays infinite and loses the comparison, so it is harmless in Python; with a finite sentinel such as `10**9` the sum could look like a real price.

## Variants
- Dijkstra with a stale skip: `network-delay-time` pushes `(d + w, nxt)` only for nodes not yet in `dist`, records `dist[node] = d` on pop, and returns `max(dist.values())` when `len(dist) == n`, else `-1`.
- Bellman-Ford with a hop limit: `cheapest-flights-within-k-stops` loops `k + 1` times. Each round copies `cost` into `nxt` and relaxes every `(u, v, price)` from the old `cost` into `nxt`, then assigns `cost = nxt`. A heap search does not fit because the cheapest route to a node may use too many stops, and the dearer route with fewer stops is the one that matters. Its snapshot is named `nxt`, which in other solutions is the neighbour.
- Minimax path, `swim-in-rising-water`: Dijkstra with the sum replaced by `max`. The solution takes the heap approach, not the binary-search-plus-BFS alternative that its comment mentions. `heap` holds `(best, r, c)`, where `best` is the highest elevation on the path so far. Pop the smallest, return `best` when `(n - 1, n - 1)` is popped, otherwise push each unvisited neighbour with `max(best, grid[nr][nc])`. It marks `visited` on push, not on pop. That is safe here because the first push of a neighbour comes from the cheapest popped cell, and `max(best, height)` cannot be lowered by any later cell, which also means no stale-entry skip is needed. Its `best` is the path cost, not the answer so far.
- Unit weights: `rotting-oranges` and the BFS problems on `bfs-shortest-paths` need only a queue.
- Dijkstra's heap is the same one as in `heap-patterns`. `minimum-spanning-tree` has the same loop with the key changed from path length to edge weight.

## Worked example
Problem: `network-delay-time`

The signal starts at `k`. The cheapest time to each node is its Dijkstra distance, and the answer is the largest of them.

```python
class Solution:

    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        dist = {}
        heap = [(0, k)]
        while heap:
            d, node = heapq.heappop(heap)
            if node in dist:
                continue
            dist[node] = d
            for nxt, w in graph[node]:
                if nxt not in dist:
                    heapq.heappush(heap, (d + w, nxt))
        return max(dist.values()) if len(dist) == n else -1
```

`graph`, `dist` and `heap` are the template's. The line `if node in dist: continue` is the stale-entry skip. The nodes are labelled from 1, so a dict stands in for a list. The final line checks that every node was reached.
