"""Flatten Binary Tree to Linked List (#114, medium)

Approach: For each node with a left child, attach its right subtree to the left
    subtree's rightmost node, then move the left subtree to the right.
Tricks: Splice the right subtree onto the left subtree's tail before overwriting
    curr.right, or it is lost; no recursion or stack needed.
Edge cases:
  - Empty tree
  - Single node
  - Left-only chain
  - Already flat tree

Time O(n), space O(1).
"""

class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """Do not return anything, modify root in-place instead."""
        curr = root
        while curr:
            if curr.left:
                # Everything in the left subtree comes before curr's right subtree in
                # preorder. So the right subtree must hang off the left subtree's last
                # node, which is its rightmost node.
                tail = curr.left
                while tail.right:
                    tail = tail.right
                tail.right = curr.right

                # Now slide the left subtree into the right slot and clear the left.
                curr.right = curr.left
                curr.left = None
            # Either way curr is done; its right pointer is the next node in preorder.
            curr = curr.right
