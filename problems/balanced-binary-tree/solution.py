"""Balanced Binary Tree (#110, easy)

Approach: Post-order DFS returning height, or -1 once an imbalance is found.
Tricks: Fold the balance check into the height return value; a separate height call per
    node is O(n²).
Edge cases:
  - Empty tree is balanced
  - Single node
  - Long skewed chain

Time O(n), space O(h).
"""


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def height(node):
            if node is None:
                return 0
            left = height(node.left)
            if left == -1:
                return -1
            right = height(node.right)
            if right == -1 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        return height(root) != -1
