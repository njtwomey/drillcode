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
        if len(edges) != n - 1:
            return False
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
        return True
