`edges` describes an undirected tree on nodes `0..n - 1`. Any node can be chosen as the root, and the height of the resulting rooted tree is the number of edges on its longest downward path.

Return the labels of all nodes whose choice as root gives the minimum possible height. The answer may be in any order.

Constraints:
- `1 <= n <= 2 * 10^4`
- `len(edges) == n - 1`
- The input is a valid tree: connected, with no repeated edges.
