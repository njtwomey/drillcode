"""Minimum Height Trees (#310, medium)

Approach: Trim leaves layer by layer, like topological sort on a tree, until one or two
    centre nodes remain.
Tricks: Minimum-height roots are the centres of the longest path, so there are at most
    two; handle n <= 2 before building the graph.
Edge cases:
  - Single node
  - Two nodes, both are answers
  - Even-length path with two centres

Time O(n), space O(n).
"""

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))
        adj = [set() for _ in range(n)]
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        # Peel the tree like an onion. The best roots are the centre of the longest
        # path, and the centre is what remains when leaves are trimmed layer by layer.
        # A tree has one or two centres, so stop once two or fewer nodes remain.
        leaves = [i for i in range(n) if len(adj[i]) == 1]
        remaining = n
        while remaining > 2:
            remaining -= len(leaves)
            next_leaves = []
            for leaf in leaves:
                nxt = adj[leaf].pop()  # a leaf has exactly one neighbour
                adj[nxt].remove(leaf)
                # Its neighbour becomes a leaf once only one edge is left.
                if len(adj[nxt]) == 1:
                    next_leaves.append(nxt)
            leaves = next_leaves
        return leaves
