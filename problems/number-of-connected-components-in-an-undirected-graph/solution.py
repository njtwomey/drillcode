"""Number of Connected Components in an Undirected Graph (#323, medium)

Approach: Start with n components; union each edge and decrement on every successful
    merge.
Tricks: Path compression and union by rank keep each operation near O(1).
Edge cases:
  - No edges (answer n)
  - Self-loops
  - Duplicate edges

Time O(n + E · α(n)), space O(n).
"""


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        # Union-find: every node starts as its own component (its own root).
        parent = list(range(n))
        size = [1] * n  # only meaningful at roots; used to keep trees shallow

        def find(x):
            while parent[x] != x:
                # Path halving: point x at its grandparent so later finds are shorter.
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        # Each successful union merges two components into one, so the answer is
        # n minus the number of merges. No graph traversal is needed.
        components = n
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                # Already connected (duplicate edge, self-loop or cycle): no merge.
                continue
            # Union by size: hang the smaller tree under the larger one.
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            components -= 1
        return components
