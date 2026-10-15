"""Delete Node in a BST (#450, medium)

Approach: Search by BST order; with two children, copy in the inorder successor's value
    and delete that node from the right subtree.
Tricks: Return the new subtree root from each recursive call so the parent relinks; the
    successor has no left child, so its own deletion is trivial.
Edge cases:
  - Empty tree or key absent
  - Deleting the root
  - Node with one child
  - Node with two children whose successor has a right child

Time O(h), space O(h).
"""

class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        # Returns the root of the subtree after deleting key, so each caller can relink
        # its child pointer to whatever now sits in that position.
        if root is None:
            return None  # key is absent

        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            # Zero or one child: the other side (or None) simply takes this node's place.
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left

            # Two children: the inorder successor (smallest value in the right subtree)
            # is the one value that keeps everything left smaller and everything right larger.
            successor = root.right
            while successor.left:
                successor = successor.left
            root.val = successor.val
            # Delete the successor's old node. It has no left child, so this is an easy case.
            root.right = self.deleteNode(root.right, successor.val)
        return root
