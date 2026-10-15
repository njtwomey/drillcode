"""Invert Binary Tree (#226, easy)

Approach: Recursively swap left and right children.
Tricks: Swapping before or after the recursive calls both work; BFS avoids deep
    recursion.
Edge cases:
  - Empty tree
  - Single node

Time O(n), space O(h).
"""


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
