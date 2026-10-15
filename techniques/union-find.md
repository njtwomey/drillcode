---
title: Union-find
area: Graphs
topics: [Graph]
problems:
  - number-of-connected-components-in-an-undirected-graph
  - graph-valid-tree
related: [graph-building-and-dfs, grid-traversal, topological-sort]
---
## Reach for it when
- The question is about connectivity or the number of components.
- Edges arrive and groups merge as you go.
- The question is whether an edge is redundant, or whether an undirected graph has a cycle.
- You need to know if a graph is a tree.

## Setup
- `parent = list(range(n))`: every node starts as its own root. Following `parent` from any node reaches its root.
- `size = [1] * n` (or a rank list): only meaningful at roots. It is used to hang the smaller tree under the larger one.
- `find(x)`: walks to the root, pointing each step at its grandparent on the way (path halving) so later finds are shorter.
- `components = n`: decremented on each successful merge. Components equal `n` minus the merges.
- Invariant: two nodes share a root if and only if an edge path joins them.
- Always union the roots, not the nodes: `ra, rb = find(a), find(b)`.

## Template
```python
def count_components(n, edges):
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    components = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        components -= 1
    return components
```

## What it removes
- It removes the adjacency list and the traversal. Each edge costs one pair of `find` calls, nearly constant time.
- It removes the parent-tracking DFS for undirected cycle detection. A shared root means the edge closes a cycle.
- It removes a recount of components at the end; the counter is kept as edges are processed.

## Pitfalls
- Unioning the nodes instead of their roots: `parent[a] = b` cuts `a` out of its old group. Components are miscounted on any input where `a` was already merged.
- Skipping the shared-root check. A duplicate edge, a self-loop or a cycle then decrements `components` and the count is too low.
- Skipping compression. The answer stays correct, but a chain of unions makes `find` linear, which is slow on large inputs.
- In graph valid tree, forgetting the edge count. Fewer than `n - 1` edges cannot connect the graph even with no cycle, so check `len(edges) != n - 1` first.
- Using it where direction matters. Union-find only answers undirected connectivity.

## Variants
- Count components: `number-of-connected-components-in-an-undirected-graph` starts `components` at `n`, skips edges whose roots match, and merges by size.
- Cycle test: `graph-valid-tree` returns `False` the moment two endpoints share a root. After the edge count check, no cycle also proves connectivity. It links `parent[ra] = rb` with no size list, which is fine with path halving.
- The same structure works on grid cells by numbering them `r * cols + c`; the catalogue solves its grid problems with a traversal instead (see `grid-traversal`).

## Worked example
Problem: `graph-valid-tree`

A tree on `n` nodes has `n - 1` edges and no cycle. The edge count is checked first, so the loop only looks for a cycle.

```python
class Solution:

    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for a, b in edges:
            ra, rb = (find(a), find(b))
            if ra == rb:
                return False
            parent[ra] = rb
        return True
```

`parent` and `find` are the template's. Here `union` is inlined: the equality of `ra` and `rb` is the "already connected" signal, and `parent[ra] = rb` joins the roots. There is no `size` list and no `components` counter, because the edge count already settles connectivity.
