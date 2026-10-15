"""Recover Binary Search Tree (#99, medium)

Approach: Iterative inorder traversal tracking the previous node; the larger side of the
    first descent and smaller side of the last are swapped back.
Tricks: Keep the first descent's earlier node and update the second on every descent;
    adjacent swaps produce just one descent.
Edge cases:
  - Swapped values adjacent in inorder (one descent)
  - Swapped root with a deep node
  - Two-node tree
  - Extreme 32-bit values

Time O(n), space O(h).
"""

# Judge notes:
# Do not return anything: modify root in place instead.


class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        """Do not return anything, modify root in-place instead."""
        # Inorder of a valid BST is increasing. Swapping two values creates one or two
        # "descents" (a value smaller than the one before it). The first misplaced node
        # is the larger side of the first descent; the second is the smaller side of the
        # last descent. If the swapped values were adjacent there is only one descent
        # and both come from it.
        first = second = prev = None
        stack = []
        curr = root
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            if prev is not None and prev.val > curr.val:
                if first is None:
                    first = prev
                second = curr
            prev = curr
            curr = curr.right

        # Swap the values, not the nodes, so no parent pointers need fixing.
        first.val, second.val = second.val, first.val
