"""Lowest Common Ancestor of a Binary Search Tree (#235, medium)

Approach: From the root: go left if both targets are smaller, right if both larger,
    otherwise the current node is the LCA.
Tricks: Use the BST ordering; the general LCA is unnecessary.
Edge cases:
  - One target is an ancestor of the other
  - a target is the root

Time O(h), space O(1).
"""


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                return node
        return None
