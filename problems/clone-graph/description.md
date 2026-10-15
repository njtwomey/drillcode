Given a reference `node` to a node of a connected, undirected graph, return a deep copy of the whole graph, as a reference to the copy of `node`. Each node has an integer `val` and a list `neighbors`; no node in the copy may be shared with the original. Return `None` if `node` is `None`.

Constraints:
- 0 to 100 nodes, with unique values `1..n` (the value equals the node's 1-based index)
- No repeated edges and no self-loops
- The graph may contain cycles
