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
        # An empty tree is a subtree of anything.
        if subRoot is None:
            return True
        # Ran out of main tree without finding a match.
        if root is None:
            return False
        # Try root as the match point; otherwise search each child. Each node starts at
        # most one _same check, hence O(m*n) worst case, though most fail quickly.
        if self._same(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def _same(self, a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
        # Exact equality, same as Same Tree: a subtree must include all descendants,
        # so a match that leaves extra children below does not count.
        if a is None and b is None:
            return True
        if a is None or b is None or a.val != b.val:
            return False
        return self._same(a.left, b.left) and self._same(a.right, b.right)
