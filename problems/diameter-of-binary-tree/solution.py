"""Post-order DFS returning height; at each node update a running max of left + right heights.

The longest path need not pass through the root, so the max is a side effect of the recursion.
Time O(n), space O(h).
"""


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        best = 0

        def height(node):
            nonlocal best
            if node is None:
                return 0
            left = height(node.left)
            right = height(node.right)
            best = max(best, left + right)
            return 1 + max(left, right)

        height(root)
        return best
