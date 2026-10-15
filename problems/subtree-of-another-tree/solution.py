"""Subtree of Another Tree (#572, easy)

Approach: For every node of the main tree, run a sameTree check against the subtree.
Tricks: O(m·n); serialising both with null markers and doing a substring search is the
    faster alternative.
Edge cases:
  - Subtree equal to the whole tree
  - Subtree is a single leaf
  - Repeated values in the main tree

Time O(m·n), space O(h).
"""


class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if subRoot is None:
            return True
        if root is None:
            return False
        if self._same(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def _same(self, a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        if a is None and b is None:
            return True
        if a is None or b is None or a.val != b.val:
            return False
        return self._same(a.left, b.left) and self._same(a.right, b.right)
