"""Walk down from the root using BST order: both targets smaller go left,
both larger go right, otherwise the current node splits them and is the LCA.

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
