"""Kruskal's algorithm with union-find.

Build all n(n-1)/2 edges with Manhattan weights, sort them, and take each edge
that joins two different components until n - 1 edges are chosen.

Time O(n^2 log n) for sorting the edges, space O(n^2).
"""


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                edges.append((dist, i, j))
        edges.sort()
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        total = taken = 0
        for dist, i, j in edges:
            root_i, root_j = find(i), find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                total += dist
                taken += 1
                if taken == n - 1:
                    break
        return total
