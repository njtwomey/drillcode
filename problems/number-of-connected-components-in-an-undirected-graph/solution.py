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
        parent = list(range(n))
        size = [1] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = n
        for a, b in edges:
            ra, rb = find(a), find(b)
            if ra == rb:
                continue
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            components -= 1
        return components
