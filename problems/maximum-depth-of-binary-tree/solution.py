"""Depth is 1 + max(depth(left), depth(right)); an empty tree has depth 0.

Time O(n), space O(h).
"""


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
