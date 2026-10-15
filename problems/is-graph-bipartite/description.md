`graph` is the adjacency list of an undirected graph with nodes `0..n - 1`: `graph[u]` lists the neighbours of `u`. The graph may be disconnected.

Return `True` if the nodes can be split into two sets so that every edge joins a node in one set to a node in the other, and `False` otherwise.

Constraints:
- `1 <= n <= 100`
- No self-loops and no parallel edges.
- If `v` is in `graph[u]` then `u` is in `graph[v]`.
