"""Graph Valid Tree (#261, medium)

Approach: A tree has exactly n - 1 edges and no cycle; union-find each edge and fail on
    a shared root.
Tricks: With the edge count checked first, finding no cycle also proves connectivity.
Edge cases:
  - n = 1 with no edges is valid
  - Too few edges means disconnected even with no cycle

Time O(n + E · α(n)), space O(n).
"""


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # A tree on n nodes has exactly n-1 edges. Fewer means disconnected. With exactly
        # n-1 edges, no cycle then implies connected, so the loop only checks for cycles.
        if len(edges) != n - 1:
            return False
        # Union-find: each node starts as its own component.
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                # Path halving keeps trees shallow, so find is near O(1) amortised.
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in edges:
            ra, rb = find(a), find(b)
            # Endpoints already connected, so this edge would close a cycle.
            if ra == rb:
                return False
            parent[ra] = rb
        return True
