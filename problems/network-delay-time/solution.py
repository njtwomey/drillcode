"""Network Delay Time (#743, medium)

Approach: Dijkstra from k with a min-heap; the answer is the largest finalised distance
    if all n nodes were reached, else -1.
Tricks: Skip heap entries for nodes already finalised, and compare the number of reached
    nodes with n to detect unreachable ones.
Edge cases:
  - A node unreachable from k
  - Shorter route using more edges
  - Zero-weight edges

Time O(E log V), space O(V + E).
"""

import heapq
from collections import defaultdict


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        # Dijkstra: weights are non-negative, so the first time a node is popped from
        # the heap its distance is final. The heap may hold stale larger entries for
        # a node; they are skipped when popped.
        dist = {}
        heap = [(0, k)]
        while heap:
            d, node = heapq.heappop(heap)
            if node in dist:
                continue
            dist[node] = d
            for nxt, w in graph[node]:
                if nxt not in dist:
                    heapq.heappush(heap, (d + w, nxt))
        # The signal reaches everyone when the farthest node gets it. A node missing
        # from dist was never reached at all.
        return max(dist.values()) if len(dist) == n else -1
