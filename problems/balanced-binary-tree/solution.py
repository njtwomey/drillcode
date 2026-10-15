"""Post-order DFS returning the subtree height, or -1 as soon as any subtree is unbalanced.

The balance check is folded into the height return value, so each node is visited once.
Time O(n), space O(h).
"""


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def height(node):
            if node is None:
                return 0
            left = height(node.left)
            if left == -1:
                return -1
            right = height(node.right)
            if right == -1 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        return height(root) != -1
