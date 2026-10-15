"""Min Cost to Connect All Points (#1584, medium)

Approach: Prim's minimum spanning tree in its O(n²) array form, tracking each point's
    cheapest edge into the tree.
Tricks: On a complete graph scan arrays instead of using a heap or building all edges;
    Kruskal with union-find also works but must sort n² edges.
Edge cases:
  - Single point costs 0
  - Negative coordinates
  - Collinear points

Time O(n²), space O(n).
"""

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        # Prim's algorithm on the complete graph, array version. cheapest[i] is the
        # lowest cost of an edge joining point i to the tree built so far. With
        # n^2 edges, scanning arrays beats a heap and avoids building the edge list.
        cheapest = [float("inf")] * n
        cheapest[0] = 0
        visited = [False] * n
        total = 0
        for _ in range(n):
            # Greedy step: pull in the outside point that is cheapest to attach.
            u = min((i for i in range(n) if not visited[i]), key=cheapest.__getitem__)
            visited[u] = True
            total += cheapest[u]
            # The tree grew, so outside points may now have a closer neighbour in it.
            for v in range(n):
                if not visited[v]:
                    dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                    if dist < cheapest[v]:
                        cheapest[v] = dist
        return total
