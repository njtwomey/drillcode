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
        if root is None:  # Base case: nothing to swap, and it ends the recursion.
            return None
        # Invert each subtree, then swap them. The right-hand side is evaluated fully
        # before assignment, so no temp variable is needed.
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
