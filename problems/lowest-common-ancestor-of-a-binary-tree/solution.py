"""Lowest Common Ancestor of a Binary Tree (#236, medium)

Approach: Post-order DFS returning whichever target is found below; a node with hits on
    both sides is the LCA.
Tricks: If only one side returns non-null, pass it up unchanged.
Edge cases:
  - One target is an ancestor of the other
  - Targets in different subtrees of the root

Time O(n), space O(h).
"""


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is None or root is p or root is q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left or right
