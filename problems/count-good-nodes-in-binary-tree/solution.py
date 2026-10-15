"""Count Good Nodes in Binary Tree (#1448, medium)

Approach: DFS passing down the maximum value seen on the path, counting nodes whose
    value is at least that maximum.
Tricks: Compare against the maximum of all ancestors, not just the parent, and seed it
    with the root value rather than 0.
Edge cases:
  - Single node
  - All negative values
  - Equal values count as good
  - Strictly decreasing chain

Time O(n), space O(h).
"""

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        # best is the largest value on the path from the root to the parent. A node is
        # good exactly when nothing above it is larger, i.e. its value is >= best.
        def dfs(node, best):
            if node is None:
                return 0
            count = 1 if node.val >= best else 0
            # Pass the updated maximum down. Seeding with root.val (not 0) keeps all-negative
            # trees correct.
            best = max(best, node.val)
            return count + dfs(node.left, best) + dfs(node.right, best)

        return dfs(root, root.val)
