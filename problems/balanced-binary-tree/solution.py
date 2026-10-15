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
        # Returns the subtree height, or -1 as a poison value meaning "unbalanced below".
        # Folding the check into the height keeps this one O(n) pass; calling height()
        # separately at every node would re-walk subtrees and cost O(n^2).
        def height(node):
            if node is None:  # An empty subtree has height 0 and is trivially balanced.
                return 0
            left = height(node.left)
            if left == -1:  # Propagate failure up without exploring the right side.
                return -1
            right = height(node.right)
            # Unbalanced if the right child failed or the two heights differ by more than 1.
            if right == -1 or abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        # Any -1 bubbled up to the root means some node somewhere was unbalanced.
        return height(root) != -1
