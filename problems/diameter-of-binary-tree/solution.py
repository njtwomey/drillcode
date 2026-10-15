"""Diameter of Binary Tree (#543, easy)

Approach: Post-order DFS returning height; update a running max of left + right heights
    at each node.
Tricks: The longest path need not pass through the root, so the max is a side effect of
    the height recursion.
Edge cases:
  - Single node (diameter 0)
  - Longest path entirely inside one subtree

Time O(n), space O(h).
"""


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        best = 0

        def height(node):
            nonlocal best
            if node is None:
                return 0
            left = height(node.left)
            right = height(node.right)
            best = max(best, left + right)
            return 1 + max(left, right)

        height(root)
        return best
