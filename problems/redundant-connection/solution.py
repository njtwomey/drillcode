"""Redundant Connection (#684, medium)

Approach: Union-find over the edges in order; the first edge whose endpoints already
    share a root closes the cycle.
Tricks: Process edges in input order so the first cycle-closing edge is also the last
    one that could be removed.
Edge cases:
  - Triangle
  - Cycle edge not at the end of the input
  - Cycle with trees hanging off it

Time O(n * α(n)), space O(n).
"""

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        parent = list(range(len(edges) + 1))  # nodes are labelled from 1

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        # Union-find over the edges in input order. If both ends of an edge already
        # share a root they are connected, so this edge closes a cycle. The graph is a
        # tree plus exactly one extra edge, so the first such edge is the answer and
        # it is also the last cycle edge in input order.
        for a, b in edges:
            root_a, root_b = find(a), find(b)
            if root_a == root_b:
                return [a, b]
            parent[root_a] = root_b
        return []  # unreachable: the input always contains one extra edge
