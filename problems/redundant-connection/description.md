A tree on nodes `1..n` had one extra edge added, producing a connected graph with exactly one cycle. `edges` lists the `n` undirected edges as `[a, b]` pairs.

Return an edge that can be removed so the remaining graph is a tree. If several edges qualify, return the one that appears last in `edges`.

Constraints:
- `3 <= n <= 1000`
- `len(edges) == n`
- No repeated edges, and the added edge joins two nodes that were not already adjacent.
