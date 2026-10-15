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
        # Longest path found so far, measured in edges (not nodes).
        best = 0

        # Returns the height of node's subtree, and records the best path bending at node.
        def height(node):
            nonlocal best  # Needed so the assignment below updates the outer variable.
            if node is None:
                return 0
            left = height(node.left)
            right = height(node.right)
            # The longest path through this node goes down both sides: left + right edges.
            # Checking every node covers paths that never touch the root.
            best = max(best, left + right)
            # A parent can only extend one branch, so report the taller side plus this node.
            return 1 + max(left, right)

        height(root)
        return best
