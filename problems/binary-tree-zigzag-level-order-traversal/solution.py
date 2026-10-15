"""Binary Tree Zigzag Level Order Traversal (#103, medium)

Approach: BFS level by level, reversing the recorded values on every second level.
Tricks: Keep the traversal order fixed and only reverse the output row, so the next
    level is still built left to right.
Edge cases:
  - Empty tree
  - Single node
  - Levels with missing children
  - Skewed chain

Time O(n), space O(n).
"""

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None:
            return []

        result = []
        # Visit each level left to right, which keeps the next level in left-to-right
        # order too. Only the recorded values are reversed on alternate levels.
        level = [root]
        reverse = False
        while level:
            values = [node.val for node in level]
            if reverse:
                values.reverse()
            result.append(values)
            reverse = not reverse
            level = [child for node in level for child in (node.left, node.right) if child]
        return result
