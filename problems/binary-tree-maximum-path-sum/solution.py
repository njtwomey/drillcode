"""Post-order DFS returning the best downward path from each node,
node + max(0, left, right). Child gains are clamped at 0 so negative subtrees
are dropped; a global best is updated with node + left + right.

Time O(n), space O(h).
"""


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        best = float("-inf")

        def gain(node):
            nonlocal best
            if node is None:
                return 0
            left = max(0, gain(node.left))
            right = max(0, gain(node.right))
            best = max(best, node.val + left + right)
            return node.val + max(left, right)

        gain(root)
        return best
