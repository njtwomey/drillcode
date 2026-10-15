"""Number of Provinces (#547, medium)

Approach: Union-find over the adjacency matrix with path halving; start with n
    components and decrement on every successful union.
Tricks: Only the upper triangle is needed because the matrix is symmetric; count merges
    rather than counting roots afterwards.
Edge cases:
  - Single city
  - No links between cities
  - Cities linked only indirectly

Time O(n² * α(n)), space O(n).
"""

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        parent = list(range(n))

        def find(x: int) -> int:
            # Path halving: point x at its grandparent while walking up, which keeps
            # the trees shallow without needing recursion.
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        # Every city starts as its own province; each union of two different
        # provinces merges them and reduces the count by one.
        count = n
        for i in range(n):
            for j in range(i + 1, n):  # the matrix is symmetric: the upper triangle suffices
                if isConnected[i][j]:
                    root_i, root_j = find(i), find(j)
                    if root_i != root_j:
                        parent[root_i] = root_j
                        count -= 1
        return count
