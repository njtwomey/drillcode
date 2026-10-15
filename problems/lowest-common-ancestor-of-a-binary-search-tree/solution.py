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
        # BST ordering lets us avoid searching both sides: the LCA is the first node where
        # p and q stop being on the same side, so one root-to-node walk is enough.
        node = root
        while node:
            # Both smaller: the split point must be in the left subtree.
            if p.val < node.val and q.val < node.val:
                node = node.left
            # Both larger: it must be in the right subtree.
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                # p and q are on different sides, or one equals node (a node can be its
                # own ancestor). Either way node is the lowest common ancestor.
                return node
        return None  # not reached when p and q are in the tree
