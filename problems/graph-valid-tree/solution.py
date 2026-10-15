"""Check edges == n - 1 first, then union-find each edge and fail if both ends share a root.

With the edge count right, finding no cycle also proves connectivity.
Time O(n + E * alpha(n)), space O(n).
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
