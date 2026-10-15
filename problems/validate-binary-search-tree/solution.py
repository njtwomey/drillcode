"""DFS passing an exclusive (low, high) range down; None means unbounded, so integer limits are safe.

Bounds come from all ancestors, not just the parent. Duplicates are invalid.
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
