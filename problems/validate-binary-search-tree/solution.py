"""Validate Binary Search Tree (#98, medium)

Approach: DFS passing an allowed (min, max) range downward, or in-order traversal
    checking strictly increasing values.
Tricks: Comparing only with the immediate parent is wrong; the bounds must come from all
    ancestors.
Edge cases:
  - Duplicates are invalid
  - Values at the integer limits, so use None or infinity as bounds

Time O(n), space O(h).
"""


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        stack = [(root, None, None)]
        while stack:
            node, low, high = stack.pop()
            if node is None:
                continue
            if (low is not None and node.val <= low) or (high is not None and node.val >= high):
                return False
            stack.append((node.left, low, node.val))
            stack.append((node.right, node.val, high))
        return True
