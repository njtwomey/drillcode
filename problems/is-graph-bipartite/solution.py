"""Is Graph Bipartite? (#785, medium)

Approach: BFS two-colouring from every unvisited node; any edge joining two equal
    colours means an odd cycle.
Tricks: Start a new search for each component, since the graph may be disconnected.
Edge cases:
  - Disconnected graph with the odd cycle in a later component
  - Isolated nodes
  - Odd versus even cycle

Time O(V + E), space O(V).
"""

from collections import deque


class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        # Two-colouring by BFS: every neighbour of a node must take the opposite
        # colour. A graph is bipartite exactly when no edge joins two equal colours
        # (equivalently, it has no odd cycle).
        colour = {}
        for start in range(len(graph)):
            # The graph may be disconnected, so every component needs its own search.
            if start in colour:
                continue
            colour[start] = 0
            queue = deque([start])
            while queue:
                curr = queue.popleft()
                for nxt in graph[curr]:
                    if nxt not in colour:
                        colour[nxt] = 1 - colour[curr]
                        queue.append(nxt)
                    elif colour[nxt] == colour[curr]:
                        return False  # an edge inside one side: odd cycle
        return True
